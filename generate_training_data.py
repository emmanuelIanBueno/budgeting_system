import pandas as pd
import random

# Generate sample training data for ML model
def generate_training_data(num_samples=500):
    data = []
    
    for i in range(num_samples):
        # Random income between 15,000 - 50,000
        income = random.randint(15000, 50000)
        
        # Budget limit is usually 80-95% of income
        budget_limit = income * random.uniform(0.80, 0.95)
        
        # Days passed in month (1-30)
        days_passed = random.randint(1, 30)
        
        # Generate spending for different categories
        food_spent = random.uniform(0, budget_limit * 0.35)
        transport_spent = random.uniform(0, budget_limit * 0.20)
        utilities_spent = random.uniform(0, budget_limit * 0.15)
        entertainment_spent = random.uniform(0, budget_limit * 0.15)
        other_spent = random.uniform(0, budget_limit * 0.15)
        
        total_spent = food_spent + transport_spent + utilities_spent + entertainment_spent + other_spent
        
        # Calculate percentage spent
        percent_spent = (total_spent / budget_limit) * 100 if budget_limit > 0 else 0
        
        # Determine if overspent (1) or not (0)
        # Overspent if: total spent > budget limit OR on track to exceed based on days
        projected_monthly_spending = (total_spent / days_passed) * 30 if days_passed > 0 else total_spent
        
        if total_spent > budget_limit or projected_monthly_spending > budget_limit * 1.05:
            overspent = 1
        else:
            overspent = 0
        
        data.append({
            'income': income,
            'budget_limit': budget_limit,
            'days_passed': days_passed,
            'food_spent': food_spent,
            'transport_spent': transport_spent,
            'utilities_spent': utilities_spent,
            'entertainment_spent': entertainment_spent,
            'other_spent': other_spent,
            'total_spent': total_spent,
            'percent_spent': percent_spent,
            'overspent': overspent
        })
    
    df = pd.DataFrame(data)
    return df

# Generate and save the dataset
print("=" * 60)
print("GENERATING TRAINING DATA FOR ML MODEL")
print("=" * 60)

print("\n📊 Creating 500 realistic budget scenarios...")
df = generate_training_data(500)

# Save to CSV
df.to_csv('budget_training_data.csv', index=False)

print(f"\n✅ Generated {len(df)} training samples!")
print(f"✅ Saved to: budget_training_data.csv")
print(f"\n📈 Dataset Summary:")
print(f"   - Overspent cases: {df['overspent'].sum()} ({df['overspent'].sum()/len(df)*100:.1f}%)")
print(f"   - Safe cases: {len(df) - df['overspent'].sum()} ({(len(df) - df['overspent'].sum())/len(df)*100:.1f}%)")

print(f"\n💡 Sample Data (First 3 rows):")
print(df[['income', 'budget_limit', 'total_spent', 'percent_spent', 'overspent']].head(3))

print("\n" + "=" * 60)
print("✅ TRAINING DATA READY!")
print("=" * 60)