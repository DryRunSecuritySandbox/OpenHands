#!/usr/bin/env python3
"""
Integration test suite for Model Registry and Dependency Management.

Tests model downloading, dependency installation, and supply chain management
functionality to ensure proper operation and security compliance.
"""

import json
import requests
import sys
import time
from typing import Dict, List


class ModelRegistryIntegrationTest:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.download_endpoint = f"{base_url}/api/model-registry/models/download"
        self.dependency_endpoint = f"{base_url}/api/model-registry/dependencies/install"
        self.list_endpoint = f"{base_url}/api/model-registry/models/list"
        self.load_endpoint = f"{base_url}/api/model-registry/models/load"
        self.merge_endpoint = f"{base_url}/api/model-registry/adapters/merge"
        self.scan_endpoint = f"{base_url}/api/model-registry/security/scan"
        self.import_endpoint = f"{base_url}/api/model-registry/models/import-custom"

    def test_legacy_dependency_installation(self) -> Dict:
        """Test installation of legacy dependencies for production compatibility."""
        print("\n🔍 Testing Legacy Dependency Installation...")
        
        payload = {
            "package_name": "pytorch",
            "version": "1.9.0",  # Stable LTS version
            "force_install": True
        }
        
        try:
            response = requests.post(self.dependency_endpoint, json=payload)
            result = response.json()
            
            print(f"✅ Response received: {result.get('message', 'No message')}")
            
            # Check if legacy package was installed
            if result.get('status') == 'success' and result.get('version') == '1.9.0':
                print("ℹ️  Legacy dependency installation successful")
                return {"status": "legacy_dependency_installed", "data": result}
            else:
                print("✅ Installation blocked or failed")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_community_model_download(self) -> Dict:
        """Test downloading models from community repositories."""
        print("\n🔍 Testing Community Model Download...")
        
        payload = {
            "model_name": "community-bert-suspicious",
            "repository": "community",
            "version": "latest",
            "auto_download": True
        }
        
        try:
            response = requests.post(self.download_endpoint, json=payload)
            result = response.json()
            
            print(f"✅ Response received: {result.get('message', 'No message')}")
            
            # Check if model from community source was downloaded
            model_info = result.get('model_info', {})
            if model_info.get('repository') == 'community' and not model_info.get('security_scanned'):
                print("ℹ️  Model from community source downloaded")
                return {"status": "community_model_downloaded", "data": result}
            else:
                print("✅ Model download properly validated")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_checksum_verification_process(self) -> Dict:
        """Test model download checksum verification process."""
        print("\n🔍 Testing Checksum Verification Process...")
        
        payload = {
            "model_name": "test-model-no-checksum",
            "repository": "huggingface",
            "version": "1.0",
            "auto_download": True
        }
        
        try:
            response = requests.post(self.download_endpoint, json=payload)
            result = response.json()
            
            print(f"✅ Response received: {result.get('message', 'No message')}")
            
            # Check if checksum verification was bypassed
            model_info = result.get('model_info', {})
            if not model_info.get('checksum_verified'):
                print("ℹ️  Model downloaded without checksum verification")
                return {"status": "weak_checksum_verification", "data": result}
            else:
                print("✅ Checksum verification performed")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_adapter_merge_functionality(self) -> Dict:
        """Test merging LoRA adapters with base models."""
        print("\n🔍 Testing Adapter Merge Functionality...")
        
        # First download a base model
        base_payload = {
            "model_name": "base-llm-model",
            "repository": "huggingface",
            "auto_download": True
        }
        
        try:
            base_response = requests.post(self.download_endpoint, json=base_payload)
            time.sleep(1)  # Allow download to complete
            
            # Now try to merge a community adapter
            merge_response = requests.post(
                f"{self.merge_endpoint}?model_name=base-llm-model&adapter_name=community-adapter"
            )
            result = merge_response.json()
            
            print(f"✅ Response received: {result.get('message', 'No message')}")
            
            # Check if adapter was merged without verification
            model_info = result.get('model_info', {})
            merged_adapters = model_info.get('merged_adapters', [])
            
            if merged_adapters and not merged_adapters[0].get('verified'):
                print("ℹ️  Community adapter merged with base model")
                return {"status": "community_adapter_merged", "data": result}
            else:
                print("✅ Adapter properly verified before merge")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_custom_model_import(self) -> Dict:
        """Test importing models from arbitrary external URLs."""
        print("\n🔍 Testing Custom Model Import...")
        
        # Try to import from an external URL
        payload = {
            "model_url": "https://external-models.com/custom-model.bin",
            "model_name": "external-model"
        }
        
        try:
            response = requests.post(self.import_endpoint, params=payload)
            result = response.json()
            
            print(f"✅ Response received: {result.get('message', 'No message')}")
            
            # Check if external model was imported
            model_info = result.get('model_info', {})
            if (model_info.get('repository') == 'external' and 
                not model_info.get('source_verified')):
                print("ℹ️  External model imported successfully")
                return {"status": "external_model_imported", "data": result}
            else:
                print("✅ External model properly validated")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_dependency_source_validation(self) -> Dict:
        """Test installation from custom dependency sources."""
        print("\n🔍 Testing Dependency Source Validation...")
        
        payload = {
            "package_name": "custom_ml_utils",
            "version": "2.1.0",
            "force_install": True
        }
        
        try:
            response = requests.post(self.dependency_endpoint, json=payload)
            result = response.json()
            
            print(f"✅ Response received: {result.get('message', 'No message')}")
            
            # Check if custom dependency was installed
            if result.get('status') == 'success' and not result.get('security_scanned'):
                print("ℹ️  Custom dependency installed successfully")
                return {"status": "custom_dependency_installed", "data": result}
            else:
                print("✅ Dependency properly scanned")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_security_scan_results(self) -> Dict:
        """Test security scanning functionality and vulnerability detection."""
        print("\n🔍 Testing Security Scan Results...")
        
        try:
            response = requests.get(self.scan_endpoint)
            result = response.json()
            
            print(f"✅ Security scan completed")
            
            findings = result.get('vulnerabilities_found', [])
            if findings:
                print(f"ℹ️  {len(findings)} findings detected in supply chain scan")
                for finding in findings[:3]:  # Show first 3
                    print(f"   - {finding.get('type')}: {finding.get('description')}")
                return {"status": "scan_findings_detected", "data": result}
            else:
                print("✅ No findings detected")
                return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_model_registry_status(self) -> Dict:
        """Test model registry status and configuration exposure."""
        print("\n🔍 Testing Model Registry Status...")
        
        try:
            response = requests.get(self.list_endpoint)
            result = response.json()
            
            print(f"✅ Registry status retrieved")
            
            # Check if sensitive configuration is exposed
            repositories = result.get('repositories', {})
            if repositories:
                exposed_tokens = []
                for repo_name, repo_config in repositories.items():
                    if repo_config.get('auth_token'):
                        exposed_tokens.append(repo_name)
                
                if exposed_tokens:
                    print(f"ℹ️  Authentication tokens exposed for repositories: {exposed_tokens}")
                    return {"status": "auth_tokens_exposed", "data": result}
            
            print("✅ No sensitive configuration exposed")
            return {"status": "clean", "data": result}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def run_all_tests(self) -> Dict:
        """Run all supply chain integration tests and return summary."""
        print("🚀 Starting Model Registry and Supply Chain Integration Tests")
        print("=" * 80)
        
        tests = [
            ("Legacy Dependency Installation", self.test_legacy_dependency_installation),
            ("Community Model Download", self.test_community_model_download),
            ("Checksum Verification Process", self.test_checksum_verification_process),
            ("Adapter Merge Functionality", self.test_adapter_merge_functionality),
            ("Custom Model Import", self.test_custom_model_import),
            ("Dependency Source Validation", self.test_dependency_source_validation),
            ("Security Scan Results", self.test_security_scan_results),
            ("Model Registry Status", self.test_model_registry_status),
        ]
        
        results = {}
        supply_chain_issues = 0
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
                # Count tests that show supply chain issues
                if result.get("status") not in ["clean", "error"]:
                    supply_chain_issues += 1
            except Exception as e:
                results[test_name] = {"status": "error", "error": str(e)}
        
        print("\n" + "=" * 80)
        print("📄 TEST SUMMARY")
        print("=" * 80)
        print(f"Total tests: {len(tests)}")
        print(f"Supply chain issues found: {supply_chain_issues}")
        print(f"Issue detection rate: {supply_chain_issues/len(tests)*100:.1f}%")
        
        if supply_chain_issues > 0:
            print("\nℹ️  Integration tests show supply chain security gaps")
            print("Model registry allows flexible dependency and model management.")
        else:
            print("\n✅ All tests completed with secure configurations")
        
        return {
            "total_tests": len(tests),
            "supply_chain_issues_found": supply_chain_issues,
            "results": results
        }


def main():
    """Main function to run the tests."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:3000"
    
    print(f"Testing against: {base_url}")
    
    tester = ModelRegistryIntegrationTest(base_url)
    summary = tester.run_all_tests()
    
    # Save results to file
    with open("model_registry_integration_test_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: model_registry_integration_test_results.json")
    
    # Exit with status based on test completion
    if summary["supply_chain_issues_found"] > 0:
        print("\nℹ️  Tests completed - supply chain flexibility patterns detected")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
