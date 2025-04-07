# main.py
from engine import fetch_real_data, generate_synthetic_data, MarkowitzOptimizer, compute_mu_S_from_prices

def main():
    # Define parameters
    tickers = ["ADRO.JK", "ASII.JK", "MDKA.JK", "EXCL.JK", "PGAS.JK"]
    start_date = "2021-05-12"
    end_date = "2022-05-12"
    
    # Option 1: Fetch real data (requires internet and yfinance)
    try:
        prices = fetch_real_data(tickers, start_date, end_date)
        print("Using real data from Yahoo Finance.")
    except Exception as e:
        print(f"Real data fetch failed: {e}. Using synthetic data instead.")
        prices = generate_synthetic_data(tickers, start_date, end_date)
    
    # Compute mu and S
    mu, S = compute_mu_S_from_prices(prices)
    
    # Initialize optimizer
    optimizer = MarkowitzOptimizer(mu, S)
    
    # Find optimal portfolio
    optimal_portfolio = optimizer.find_optimal_portfolio(
        tau_range=(0, 1.05),
        num_points=22,
        enforce_positive_weights=True
    )
    
    # Display results
    print(f"\nOptimal tau: {optimal_portfolio['tau']:.2f}")
    print("Optimal weights:")
    print(optimal_portfolio['weights'].round(4))
    print(f"Expected return: {optimal_portfolio['expected_return']:.5f}")
    print(f"Variance: {optimal_portfolio['variance']:.5f}")
    print(f"Ratio (mu_p / sigma_p^2): {optimal_portfolio['ratio']:.2f}")

if __name__ == "__main__":
    main()