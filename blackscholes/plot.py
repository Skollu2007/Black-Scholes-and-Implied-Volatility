import matplotlib.pyplot as plt

def plot_iv_surface(moneyness, dtes, ivs):
    fig = plt.figure(figsize=(12,8), dpi=100)
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_trisurf(moneyness, dtes, ivs, cmap='viridis', linewidth=0.1, antialiased=True, alpha=0.8)
    
    cbar= fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, pad=0.1)
    cbar.set_label('Implied Volatility, rotation=270, labelpad=15')

    ax.set_xlabel('Moneyness', labelpad=10)
    ax.set_ylabel('Time to Expiration', labelpad=10)
    ax.set_zlabel('Implied Volatility', labelpad=10)

    plt.title('Implied Volatility Surface', pad=20, size=14)
    ax.view_init(elev=30, azim=45)  
    plt.tight_layout()
    plt.xlim(0.5, 2.4)
    plt.show()