#!/usr/bin/env python3
"""
Script para verificar el despliegue en Render
Uso: python scripts/verify_deployment.py <URL_BASE>
Ejemplo: python scripts/verify_deployment.py https://producto-datos-ml-api.onrender.com
"""

import sys
import requests
import json
from typing import Dict, Any

def test_health_endpoint(base_url: str) -> Dict[str, Any]:
    """Probar endpoint /health"""
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        return {
            "status": "success" if response.status_code == 200 else "failed",
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "response_time": response.elapsed.total_seconds()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def test_docs_endpoint(base_url: str) -> Dict[str, Any]:
    """Probar endpoint /docs (Swagger UI)"""
    try:
        response = requests.get(f"{base_url}/docs", timeout=30)
        return {
            "status": "success" if response.status_code == 200 else "failed",
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def test_predict_endpoint(base_url: str) -> Dict[str, Any]:
    """Probar endpoint /predict con imagen de ejemplo"""
    try:
        # Imagen de ejemplo de Wikipedia (pequeña, pública)
        test_payload = {
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/320px-HST-SM4.jpeg"
        }
        
        response = requests.post(
            f"{base_url}/predict",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=60  # Más tiempo para predicción
        )
        
        result = {
            "status": "success" if response.status_code == 200 else "failed",
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds()
        }
        
        if response.status_code == 200:
            resp_json = response.json()
            result["prediction"] = resp_json.get("prediction")
            result["has_probabilities"] = "probabilities" in resp_json
            result["has_metadata"] = "metadata" in resp_json
        else:
            result["error_response"] = response.text[:200]
            
        return result
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/verify_deployment.py <URL_BASE>")
        print("Ejemplo: python scripts/verify_deployment.py https://producto-datos-ml-api.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip("/")
    
    print(f"🔍 Verificando despliegue en: {base_url}")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1️⃣  Probando /health...")
    health_result = test_health_endpoint(base_url)
    if health_result["status"] == "success":
        print(f"   ✅ Health OK ({health_result['response_time']:.2f}s)")
        print(f"   📋 Respuesta: {health_result['response']}")
    else:
        print(f"   ❌ Health FAILED: {health_result}")
    
    # Test 2: Documentation
    print("\n2️⃣  Probando /docs...")
    docs_result = test_docs_endpoint(base_url)
    if docs_result["status"] == "success":
        print(f"   ✅ Docs OK")
        print(f"   📄 Content-Type: {docs_result['content_type']}")
    else:
        print(f"   ❌ Docs FAILED: {docs_result}")
    
    # Test 3: Prediction
    print("\n3️⃣  Probando /predict...")
    predict_result = test_predict_endpoint(base_url)
    if predict_result["status"] == "success":
        print(f"   ✅ Predict OK ({predict_result['response_time']:.2f}s)")
        print(f"   🎯 Predicción: {predict_result.get('prediction', 'N/A')}")
        print(f"   📊 Tiene probabilidades: {predict_result.get('has_probabilities', False)}")
        print(f"   🔢 Tiene metadata: {predict_result.get('has_metadata', False)}")
    else:
        print(f"   ❌ Predict FAILED: {predict_result}")
    
    # Resumen
    print("\n" + "=" * 60)
    all_success = all([
        health_result["status"] == "success",
        docs_result["status"] == "success", 
        predict_result["status"] == "success"
    ])
    
    if all_success:
        print("🎉 ¡DESPLIEGUE EXITOSO! Todos los endpoints funcionan.")
        print(f"\n🔗 URLs importantes:")
        print(f"   • API: {base_url}")
        print(f"   • Health: {base_url}/health")
        print(f"   • Docs: {base_url}/docs")
        print(f"   • Predict: {base_url}/predict")
    else:
        print("⚠️  Hay problemas con el despliegue. Revisa los logs de Render.")

if __name__ == "__main__":
    main()
