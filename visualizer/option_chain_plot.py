# visualizer/option_chain_plot.py

import matplotlib.pyplot as plt

def generate_oi_chart(option_data: dict, symbol: str, atm_strike: int, save_path='oi_chart.png'):
    """
    Plots Option Chain OI chart for CALLs and PUTs
    :param option_data: {'calls': [...], 'puts': [...]}
    :param symbol: e.g., NIFTY
    :param atm_strike: ATM strike for highlight
    :param save_path: PNG path to save
    """
    calls = option_data['calls']
    puts = option_data['puts']
    
    strikes = [c['strike'] for c in calls]
    call_oi = [c['oi'] for c in calls]
    put_oi = [p['oi'] for p in puts]

    # Chart style
    fig, ax = plt.subplots(figsize=(10, len(strikes) * 0.5))
    y_pos = list(range(len(strikes)))

    # Bars
    ax.barh(y_pos, call_oi, color='skyblue', edgecolor='blue', label='CALL OI')
    ax.barh(y_pos, [-v for v in put_oi], color='lightcoral', edgecolor='darkred', label='PUT OI')

    # Highlight ATM
    if atm_strike in strikes:
        atm_index = strikes.index(atm_strike)
        ax.barh(atm_index, call_oi[atm_index], color='green')
        ax.barh(atm_index, -put_oi[atm_index], color='green')

    # Labels & Lines
    ax.set_yticks(y_pos)
    ax.set_yticklabels([str(s) for s in strikes])
    ax.axvline(0, color='black')
    ax.set_xlabel('Open Interest')
    ax.set_title(f'Option Chain OI – {symbol.upper()}')

    ax.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    
    return save_path
