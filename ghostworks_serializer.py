"""
GhostWorks → Gemma Context Serializer
LuxVerso Research Initiative — Vinicius Buri
Version: 1.0 | May 2026

Converte os outputs do pipeline GhostWorks em um JSON contextual
estruturado para alimentar o Gemma 4 como agente de inteligência territorial.

USO:
    from ghostworks_serializer import serialize_session
    context = serialize_session("aral_sea", session_dir="/content/")
    print(context)  # JSON pronto para o Gemma
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────────
# METADADOS DAS REGIÕES CONHECIDAS
# ─────────────────────────────────────────────
REGION_METADATA = {
    "aral_sea": {
        "name": "Aral Sea",
        "country": "Kazakhstan / Uzbekistan",
        "biome": "Central Asian Arid Steppe",
        "lat_center": 45.0,
        "lon_center": 59.0,
        "known_context": (
            "Historically one of the world's largest lakes. "
            "Experienced catastrophic water body retraction since the 1960s "
            "due to Soviet-era irrigation diversion. Currently undergoing "
            "partial ecological reorganization in the northern basin (Kazakhstan). "
            "Serves as a global benchmark for large-scale territorial collapse."
        ),
        "primary_driver_hypothesis": "Hydrological collapse + arid land succession"
    },
    "matopiba": {
        "name": "MATOPIBA",
        "country": "Brazil",
        "biome": "Cerrado (Brazilian Savanna)",
        "lat_center": -12.0,
        "lon_center": -46.0,
        "known_context": (
            "Agricultural frontier encompassing Maranhão, Tocantins, Piauí, and Bahia states. "
            "One of the most dynamic agricultural expansion zones in the world. "
            "High soy and cotton production growth since the 2000s. "
            "Under intense pressure from deforestation, water stress, and land-use change. "
            "Considered a live territorial transformation in progress."
        ),
        "primary_driver_hypothesis": "Agribusiness expansion + Cerrado deforestation"
    }
}


# ─────────────────────────────────────────────
# FUNÇÕES DE LEITURA
# ─────────────────────────────────────────────

def _load_csv_safe(path: str) -> pd.DataFrame | None:
    """Carrega CSV com fallback silencioso."""
    try:
        return pd.read_csv(path)
    except Exception:
        return None


def _summarize_trajectory(df: pd.DataFrame) -> dict:
    """Resume a trajetória temporal STT."""
    if df is None or df.empty:
        return {}
    return {
        "years": df["ano"].tolist(),
        "stt_mean": [round(v, 4) for v in df["stt_mean"].tolist()],
        "stt_p90":  [round(v, 4) for v in df["stt_p90"].tolist()],
        "stt_std":  [round(v, 4) for v in df["stt_std"].tolist()],
        "trend": _compute_trend(df["stt_mean"].tolist()),
        "peak_year": int(df.loc[df["stt_mean"].idxmax(), "ano"]),
        "peak_stt":  round(df["stt_mean"].max(), 4),
    }


def _summarize_trajectory_relative(df: pd.DataFrame) -> dict:
    """Resume a trajetória de variação relativa anual."""
    if df is None or df.empty:
        return {}
    return {
        "periods": df["par"].tolist(),
        "stt_delta": [round(v, 4) for v in df["stt_relativo"].tolist()],
        "max_delta_period": df.loc[df["stt_relativo"].idxmax(), "par"],
        "max_delta_value":  round(df["stt_relativo"].max(), 4),
    }


def _summarize_outliers(df: pd.DataFrame) -> dict:
    """Resume os outliers detectados."""
    if df is None or df.empty:
        return {}
    outliers = df[df["is_outlier"] == True]
    return {
        "total_points_analyzed": len(df),
        "outlier_count": len(outliers),
        "outlier_fraction": round(len(outliers) / len(df), 4),
        "outlier_stt_mean":  round(outliers["stt"].mean(), 4) if len(outliers) > 0 else None,
        "outlier_stt_max":   round(outliers["stt"].max(),  4) if len(outliers) > 0 else None,
        "outlier_score_mean": round(outliers["outlier_score"].mean(), 4) if len(outliers) > 0 else None,
        "ndvi_delta_mean": round(df["ndvi_delta"].mean(), 4),
        "sar_delta_mean":  round(df["sar_delta"].mean(), 4),
    }


def _summarize_clusters(df: pd.DataFrame) -> dict:
    """Resume a distribuição de clusters."""
    if df is None or df.empty:
        return {}
    cluster_summary = (
        df.groupby("cluster")
        .agg(
            count=("stt", "count"),
            stt_mean=("stt", "mean"),
            ndvi_delta_mean=("ndvi_delta", "mean"),
            sar_delta_mean=("sar_delta", "mean"),
        )
        .round(4)
        .reset_index()
        .to_dict(orient="records")
    )
    return {
        "n_clusters": df["cluster"].nunique(),
        "total_points": len(df),
        "clusters": cluster_summary,
        "dominant_cluster": int(df["cluster"].value_counts().idxmax()),
    }


def _summarize_similar_regions(df: pd.DataFrame) -> dict:
    """Resume as regiões similares por embedding."""
    if df is None or df.empty:
        return {}
    top = df.nlargest(5, "similarity")
    return {
        "total_similar_regions": len(df),
        "top_5": [
            {
                "lat": round(row.lat, 4),
                "lon": round(row.lon, 4),
                "similarity": round(row.similarity, 4),
            }
            for row in top.itertuples()
        ],
        "similarity_mean": round(df["similarity"].mean(), 4),
        "similarity_max":  round(df["similarity"].max(), 4),
    }


def _compute_trend(values: list) -> str:
    """Tendência simples por regressão linear."""
    if len(values) < 2:
        return "insufficient_data"
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    if slope > 0.005:
        return "accelerating"
    elif slope > 0.001:
        return "increasing"
    elif slope < -0.005:
        return "decelerating"
    elif slope < -0.001:
        return "decreasing"
    else:
        return "stable"


# ─────────────────────────────────────────────
# SERIALIZADOR PRINCIPAL
# ─────────────────────────────────────────────

def serialize_session(
    region_key: str,
    session_dir: str = "/content/",
    session_name: str = None,
) -> str:
    """
    Serializa uma sessão GhostWorks em JSON contextual para o Gemma.

    Args:
        region_key:   "aral_sea" ou "matopiba"
        session_dir:  diretório onde estão os CSVs exportados
        session_name: prefixo dos arquivos (auto-detectado se None)

    Returns:
        str: JSON formatado pronto para injetar no prompt do Gemma
    """
    base = Path(session_dir)
    meta = REGION_METADATA.get(region_key, {})

    # Auto-detectar prefixo
    if session_name is None:
        prefixes = {
            "aral_sea": "ghostworks_aralsea_explorer",
            "matopiba": "ghostworks_explorer_sessao1",
        }
        session_name = prefixes.get(region_key, region_key)

    # ── Carregar arquivos ──
    suffix_map = {
        "aral_sea": {
            "trajectory":          f"{session_name}_trajectory.csv",
            "trajectory_relative": f"{session_name}_trajectory_relative.csv",
            "outliers":            f"{session_name}_outliers.csv",
            "clusters":            f"{session_name}_clusters.csv",
            "similar_regions":     f"{session_name}_similar_regions.csv",
        },
        "matopiba": {
            "trajectory":          f"{session_name}_trajectory_matopiba.csv",
            "trajectory_relative": f"{session_name}_trajectory_relative_matopiba.csv",
            "outliers":            f"{session_name}_outliers_matopiba.csv",
            "clusters":            None,  # não gerado nessa sessão
            "similar_regions":     f"{session_name}_similar_regions.csv",
        },
    }

    files = suffix_map.get(region_key, {})

    df_traj     = _load_csv_safe(base / files["trajectory"])          if files.get("trajectory") else None
    df_traj_rel = _load_csv_safe(base / files["trajectory_relative"]) if files.get("trajectory_relative") else None
    df_out      = _load_csv_safe(base / files["outliers"])             if files.get("outliers") else None
    df_clust    = _load_csv_safe(base / files["clusters"])             if files.get("clusters") else None
    df_sim      = _load_csv_safe(base / files["similar_regions"])      if files.get("similar_regions") else None

    # ── Montar contexto ──
    context = {
        "ghostworks_session": {
            "region": meta.get("name", region_key),
            "country": meta.get("country", ""),
            "biome": meta.get("biome", ""),
            "coordinates_center": {
                "lat": meta.get("lat_center"),
                "lon": meta.get("lon_center"),
            },
            "known_context": meta.get("known_context", ""),
            "primary_driver_hypothesis": meta.get("primary_driver_hypothesis", ""),
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "tti_definition": (
                "TTI (Territorial Transformation Index) = 1 − cosine_similarity(emb_t1, emb_t2). "
                "Based on 64-dimensional AlphaEarth Foundation satellite embeddings (Google DeepMind). "
                "Label-agnostic: detects change regardless of type. "
                "Scale: 0 (no change) → 1 (maximum transformation)."
            ),
        },
        "temporal_trajectory": _summarize_trajectory(df_traj),
        "annual_delta": _summarize_trajectory_relative(df_traj_rel),
        "anomaly_detection": _summarize_outliers(df_out),
        "spatial_clustering": _summarize_clusters(df_clust),
        "similar_regions": _summarize_similar_regions(df_sim),
    }

    return json.dumps(context, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# TESTE RÁPIDO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Substitua session_dir pelo caminho dos seus CSVs
    ctx = serialize_session("aral_sea", session_dir="./")
    print(ctx)
