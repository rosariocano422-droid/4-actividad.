import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Capas apiladas - Solido de revolucion", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e6e6e6; }
    </style>
    """,
    unsafe_allow_html=True,
)

def f(x):
    return 6 * x - x**2

def g(x):
    return 2 * x

VOL_EXACTO = 2 * np.pi * (4 * 4**3 / 3 - 4**4 / 4)

st.sidebar.title("Controles")
n = st.sidebar.slider("Numero de capas (n)", min_value=4, max_value=60, value=16, step=1)
mostrar_tabla = st.sidebar.checkbox("Mostrar tabla de capas", value=True)

st.title("Capas apiladas de un solido de revolucion")
st.caption("Region entre f(x) = 6x - x^2 (arriba) y g(x) = 2x (abajo), girada alrededor del eje y")

dx = 4.0 / n
xs = (np.arange(n) + 0.5) * dx
radios = xs
alturas = f(xs) - g(xs)
bases_inf = g(xs)
bases_sup = f(xs)
volumenes = 2 * np.pi * radios * alturas * dx

theta = np.linspace(0, 2 * np.pi, 40)
colores = np.linspace(0, 1, n)

fig = go.Figure()

ancho_visible = dx * 0.75

for i in range(n):
    r_in = xs[i] - ancho_visible / 2
    r_out = xs[i] + ancho_visible / 2
    z_bot = bases_inf[i]
    z_top = bases_sup[i]

    Theta, Z = np.meshgrid(theta, [z_bot, z_top])
    X = r_out * np.cos(Theta)
    Y = Z
    Zc = r_out * np.sin(Theta)

    color_val = colores[i]
    fig.add_trace(
        go.Surface(
            x=X, y=Y, z=Zc,
            surfacecolor=np.full_like(X, color_val),
            colorscale="Turbo",
            cmin=0, cmax=1,
            showscale=False,
            opacity=0.95,
        )
    )

fig.update_layout(
    scene=dict(
        xaxis_title="x",
        yaxis_title="y (eje de rotacion)",
        zaxis_title="z",
        aspectmode="data",
        bgcolor="#0e1117",
        xaxis=dict(color="#e6e6e6", gridcolor="#333"),
        yaxis=dict(color="#e6e6e6", gridcolor="#333"),
        zaxis=dict(color="#e6e6e6", gridcolor="#333"),
    ),
    paper_bgcolor="#0e1117",
    font=dict(color="#e6e6e6"),
    margin=dict(l=0, r=0, t=10, b=0),
    height=520,
)

col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.plotly_chart(fig, use_container_width=True)

with col_der:
    st.metric("Volumen aproximado (suma de capas)", f"{volumenes.sum():.2f} u3")
    st.metric("Volumen exacto (integral)", f"{VOL_EXACTO:.2f} u3")
    diferencia = abs(VOL_EXACTO - volumenes.sum())
    st.metric("Diferencia", f"{diferencia:.3f} u3")
    st.write(f"Con **{n} capas**, cada una mide Δx = {dx:.3f} de espesor.")
    st.write("A mas capas, la aproximacion se acerca mas al valor exacto de la integral.")

if mostrar_tabla:
    st.subheader("Tabla de capas")
    st.dataframe(
        {
            "Capa": list(range(1, n + 1)),
            "Radio (x)": np.round(radios, 3),
            "Altura f(x)-g(x)": np.round(alturas, 3),
            "Espesor dx": np.round(np.full(n, dx), 3),
            "Volumen de la capa": np.round(volumenes, 3),
        },
        use_container_width=True,
        height=300,
    )
