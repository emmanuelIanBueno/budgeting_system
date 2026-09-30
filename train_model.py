import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

print("=" * 70)
print("TRAINING BUDGET OVERSPENDING PREDICTION MODEL")
print("=" * 70)

# Load the training data
print("\n📂 Step 1: Loading training data...")
df = pd.read_csv('budget_training_data.csv')
print(f"   ✅ Loaded {len(df)} samples")

# Prepare features (X) and target (y)
print("\n🔧 Step 2: Preparing features...")
features = ['income', 'budget_limit', 'days_passed', 'food_spent', 
            'transport_spent', 'utilities_spent', 'entertainment_spent', 
            'other_spent', 'total_spent', 'percent_spent']

X = df[features]
y = df['overspent']
print(f"   ✅ Using {len(features)} features")

# Split data: 80% training, 20% testing
print("\n✂️  Step 3: Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   ✅ Training samples: {len(X_train)}")
print(f"   ✅ Testing samples: {len(X_test)}")

# Train Random Forest model
print("\n🤖 Step 4: Training Random Forest model...")
print("   (This may take 10-20 seconds...)")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("   ✅ Model trained successfully!")

# Make predictions
print("\n🎯 Step 5: Testing model accuracy...")
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n   {'🏆 MODEL ACCURACY: ' + str(round(accuracy * 100, 2)) + '%':^70}")

# Detailed metrics
print("\n📊 Step 6: Detailed Performance Metrics:")
print("=" * 70)
print(classification_report(y_test, y_pred, target_names=['Safe (No Overspend)', 'Will Overspend']))
print("=" * 70)

# Confusion Matrix
print("\n📈 Step 7: Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"   ✅ True Negatives (Correctly predicted Safe): {cm[0][0]}")
print(f"   ⚠️  False Positives (Wrongly predicted Overspend): {cm[0][1]}")
print(f"   ⚠️  False Negatives (Wrongly predicted Safe): {cm[1][0]}")
print(f"   ✅ True Positives (Correctly predicted Overspend): {cm[1][1]}")

# Feature importance
print("\n💡 Step 8: Most Important Features for Prediction:")
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(5).iterrows():
    bar_length = int(row['importance'] * 50)
    bar = '█' * bar_length
    print(f"   {row['feature']:20s} {bar} {row['importance']:.4f}")

# Save the model
print("\n💾 Step 9: Saving trained model...")
with open('budget_model.pkl', 'wb') as file:
    pickle.dump(model, file)
print("   ✅ Model saved as: budget_model.pkl")

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)
print(f"\n🎉 Your ML model is ready to predict overspending!")
print(f"📊 Final Accuracy: {accuracy * 100:.2f}%")
print(f"💾 Model saved and ready to use in your web app!")
print("\n" + "=" * 70)