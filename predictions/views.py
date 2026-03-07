"""
Views for predictions app - handles ML predictions and rendering.
"""
import pickle
import numpy as np
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from .models import Prediction


# Load ML models once at startup (efficient)
def load_models():
    """Load all pre-trained models from Models directory."""
    models = {}
    try:
        models['heart'] = pickle.load(open(settings.MODELS_DIR / 'heart_disease_model.sav', 'rb'))
        models['lung'] = pickle.load(open(settings.MODELS_DIR / 'lungs_disease_model.sav', 'rb'))
        models['diabetes'] = pickle.load(open(settings.MODELS_DIR / 'diabetes_model.sav', 'rb'))
        models['parkinsons'] = pickle.load(open(settings.MODELS_DIR / 'parkinsons_model.sav', 'rb'))
        models['thyroid'] = pickle.load(open(settings.MODELS_DIR / 'Thyroid_model.sav', 'rb'))
    except Exception as e:
        print(f"Error loading models: {e}")
    return models

# Global models dictionary
ML_MODELS = load_models()


def home(request):
    """Homepage with overview of available predictions."""
    context = {
        'diseases': [
            {
                'name': 'Heart Disease',
                'url': 'predictions:heart_disease',
                'icon': '❤️',
                'description': 'Predict risk of heart disease based on clinical parameters'
            },
            {
                'name': 'Lung Cancer',
                'url': 'predictions:lung_cancer',
                'icon': '🫁',
                'description': 'Assess lung cancer risk from patient symptoms'
            },
            {
                'name': 'Diabetes',
                'url': 'predictions:diabetes',
                'icon': '🩸',
                'description': 'Evaluate diabetes likelihood using health metrics'
            },
            {
                'name': 'Parkinsons Disease',
                'url': 'predictions:parkinsons',
                'icon': '🧠',
                'description': 'Detect Parkinsons based on voice measurements'
            },
            {
                'name': 'Thyroid Disorder',
                'url': 'predictions:thyroid',
                'icon': '🦋',
                'description': 'Identify thyroid conditions from lab results'
            },
        ]
    }
    return render(request, 'predictions/home.html', context)


def heart_disease_prediction(request):
    """Heart disease prediction view."""
    if request.method == 'POST':
        try:
            # Extract all 13 features for heart disease model
            features = [
                float(request.POST.get('age')),
                float(request.POST.get('sex')),
                float(request.POST.get('cp')),
                float(request.POST.get('trestbps')),
                float(request.POST.get('chol')),
                float(request.POST.get('fbs')),
                float(request.POST.get('restecg')),
                float(request.POST.get('thalach')),
                float(request.POST.get('exang')),
                float(request.POST.get('oldpeak')),
                float(request.POST.get('slope')),
                float(request.POST.get('ca')),
                float(request.POST.get('thal')),
            ]
            
            # Make prediction
            input_array = np.array([features])
            prediction = ML_MODELS['heart'].predict(input_array)[0]
            
            # Interpret result
            if prediction == 1:
                result = "⚠️ Heart Disease Detected"
                result_class = "danger"
            else:
                result = "✅ No Heart Disease"
                result_class = "success"
            
            # Save to database
            Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                disease_type='heart',
                input_data={f'feature_{i}': val for i, val in enumerate(features)},
                prediction_result=result,
            )
            
            context = {
                'disease': 'Heart Disease',
                'result': result,
                'result_class': result_class,
                'prediction_value': int(prediction),
            }
            return render(request, 'predictions/result.html', context)
            
        except Exception as e:
            messages.error(request, f"Error processing prediction: {str(e)}")
            return render(request, 'predictions/heart_disease.html')
    
    return render(request, 'predictions/heart_disease.html')


def lung_cancer_prediction(request):
    """Lung cancer prediction view."""
    if request.method == 'POST':
        try:
            # Extract features (adjust based on your actual lung cancer model features)
            features = [
                float(request.POST.get('gender')),
                float(request.POST.get('age')),
                float(request.POST.get('smoking')),
                float(request.POST.get('yellow_fingers')),
                float(request.POST.get('anxiety')),
                float(request.POST.get('peer_pressure')),
                float(request.POST.get('chronic_disease')),
                float(request.POST.get('fatigue')),
                float(request.POST.get('allergy')),
                float(request.POST.get('wheezing')),
                float(request.POST.get('alcohol')),
                float(request.POST.get('coughing')),
                float(request.POST.get('shortness_of_breath')),
                float(request.POST.get('swallowing_difficulty')),
                float(request.POST.get('chest_pain')),
            ]
            
            input_array = np.array([features])
            prediction = ML_MODELS['lung'].predict(input_array)[0]
            
            if prediction == 1:
                result = "⚠️ Lung Cancer Risk Detected"
                result_class = "danger"
            else:
                result = "✅ Low Lung Cancer Risk"
                result_class = "success"
            
            Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                disease_type='lung',
                input_data={f'feature_{i}': val for i, val in enumerate(features)},
                prediction_result=result,
            )
            
            context = {
                'disease': 'Lung Cancer',
                'result': result,
                'result_class': result_class,
                'prediction_value': int(prediction),
            }
            return render(request, 'predictions/result.html', context)
            
        except Exception as e:
            messages.error(request, f"Error processing prediction: {str(e)}")
            return render(request, 'predictions/lung_cancer.html')
    
    return render(request, 'predictions/lung_cancer.html')


def diabetes_prediction(request):
    """Diabetes prediction view."""
    if request.method == 'POST':
        try:
            # Extract all 8 features for diabetes model
            features = [
                float(request.POST.get('pregnancies')),
                float(request.POST.get('glucose')),
                float(request.POST.get('blood_pressure')),
                float(request.POST.get('skin_thickness')),
                float(request.POST.get('insulin')),
                float(request.POST.get('bmi')),
                float(request.POST.get('dpf')),
                float(request.POST.get('age')),
            ]
            
            # Make prediction
            input_array = np.array([features])
            prediction = ML_MODELS['diabetes'].predict(input_array)[0]
            
            # Interpret result
            if prediction == 1:
                result = "⚠️ Diabetes Detected"
                result_class = "danger"
            else:
                result = "✅ No Diabetes"
                result_class = "success"
            
            # Save to database
            Prediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                disease_type='diabetes',
                input_data={f'feature_{i}': val for i, val in enumerate(features)},
                prediction_result=result,
            )
            
            context = {
                'disease': 'Diabetes',
                'result': result,
                'result_class': result_class,
                'prediction_value': int(prediction),
            }
            return render(request, 'predictions/result.html', context)
            
        except Exception as e:
            messages.error(request, f"Error processing prediction: {str(e)}")
            return render(request, 'predictions/diabetes.html')
    
    return render(request, 'predictions/diabetes.html')


def parkinsons_prediction(request):
    """Parkinsons prediction view."""
    if request.method == 'POST':
        messages.info(request, "Parkinsons prediction coming soon!")
        return render(request, 'predictions/parkinsons.html')
    
    return render(request, 'predictions/parkinsons.html')


def thyroid_prediction(request):
    """Thyroid prediction view."""
    if request.method == 'POST':
        messages.info(request, "Thyroid prediction coming soon!")
        return render(request, 'predictions/thyroid.html')
    
    return render(request, 'predictions/thyroid.html')
