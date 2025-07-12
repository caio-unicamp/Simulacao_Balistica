import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

# Dados para uma Pistola 9mm FMJ unindo diversas fontes

# === Parâmetros Físicos ===
g = 9.81  # gravidade (m/s²)
rho = 1.225  # densidade do ar (kg/m³)
Cd = 0.295  # coeficiente de arrasto para uma esfera
d = 0.00902  # diâmetro do projétil (m)
A = np.pi * (d/2)**2  # área frontal (m²) da bala será um círculo de diâmetro 0,00902m 
m = 0.008  # massa do projétil (kg)

# === Condições Iniciais ===
v0 = 358.0  # velocidade inicial (m/s)
theta_deg = 45.0
theta = np.radians(theta_deg)
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)
y0 = [0, 0, vx0, vy0]  # [x, y, vx, vy]

# === Sistema de EDOs com resistência do ar ===
def projectile_with_drag(t, y):
    x, y_pos, vx, vy = y
    v = np.sqrt(vx**2 + vy**2)
    # Força de arrasto sofrida pelo projétil (Usando situação em que o arrasto é não viscoso)
    # é proporcional à massa de ar deslocada pelo projétil
    # e à velocidade do projétil, daí
    # F ~ Δm⋅v = (ρAv)*v = ρAv²
    # Para igualdade adicionamos um fator de arrasto empírico Cd
    drag = 0.5 * rho * Cd * A * v
    ax = -drag * vx / m
    ay = -g - (drag * vy / m)
    return [vx, vy, ax, ay]

# === Evento para detectar o impacto com o solo ===
def hit_ground(t, y):
    return y[1]  # altura y = 0
hit_ground.terminal = True
hit_ground.direction = -1  # só detectar quando estiver descendo

# === Intervalo de simulação ===
t_span = (0, 60)
# t_eval = np.linspace(*t_span, 5000)

# === Resolver o sistema de EDO ===
sol = solve_ivp(
    projectile_with_drag,
    t_span,
    y0,
    events=hit_ground,
    rtol=1e-8,
    atol=1e-8
)

# === Resultados ===
print("Eventos detectados:", sol.t_events)
impact_time = sol.t_events[0][0]

vx_interp = interp1d(sol.t, sol.y[2])
vy_interp = interp1d(sol.t, sol.y[3])
vx_impact = float(vx_interp(impact_time))
vy_impact = float(vy_interp(impact_time))
impact_velocity = np.sqrt(vx_impact**2 + vy_impact**2)

apex_index = np.argmax(sol.y[1])
apex_velocity = np.sqrt(sol.y[2][apex_index]**2 + sol.y[3][apex_index]**2)

print(f"🟢 Velocidade no ponto mais alto: {apex_velocity:.2f} m/s")
print(f"🔴 Velocidade no impacto com o solo: {impact_velocity:.2f} m/s")
print(f"⏱ Tempo de voo até o impacto: {impact_time:.2f} s")

# === Gráficos ===
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

# Trajetória
ax[0].plot(sol.y[0], sol.y[1])
ax[0].set_title("Trajetória do Projétil com Resistência do Ar")
ax[0].set_xlabel("Distância horizontal (m)")
ax[0].set_ylabel("Altura (m)")
ax[0].grid(True)

# Velocidade
speed = np.sqrt(sol.y[2]**2 + sol.y[3]**2)
ax[1].plot(sol.t, speed, label="Velocidade")
ax[1].axvline(sol.t[apex_index], color='orange', linestyle='--', label="Ponto mais alto")
ax[1].axvline(impact_time, color='red', linestyle='--', label="Impacto")
ax[1].set_title("Velocidade ao Longo do Tempo")
ax[1].set_xlabel("Tempo (s)")
ax[1].set_ylabel("Velocidade (m/s)")
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()
