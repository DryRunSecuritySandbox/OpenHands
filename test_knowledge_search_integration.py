#!/usr/bin/env python3
"""
Integration Test Suite for OpenHands Enterprise Knowledge Search Service

Comprehensive testing of semantic search, vector embeddings, multi-tenant RAG capabilities,
and enterprise-grade knowledge management with intelligent information retrieval.
"""

import json
import requests
import time
from typing import Dict, List
from datetime import datetime


class KnowledgeSearchIntegrationTest:
    """Integration test suite for enterprise knowledge search and vector embedding functionality."""

    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.search_endpoint = f"{base_url}/api/knowledge-search/semantic-search"
        self.vector_endpoint = f"{base_url}/api/knowledge-search/vector-similarity"
        self.embedding_endpoint = f"{base_url}/api/knowledge-search/generate-embedding"
        self.inversion_endpoint = f"{base_url}/api/knowledge-search/invert-embedding"
        self.status_endpoint = f"{base_url}/api/knowledge-search/knowledge-base-status"

        print("🚀 Enterprise Knowledge Search Integration Test Suite")
        print(f"📡 Testing against: {base_url}")
        print("=" * 80)

    def test_cross_tenant_semantic_search(self) -> Dict:
        """Test cross-tenant semantic search capabilities."""
        print("\n🔍 Testing Cross-Tenant Semantic Search...")

        try:
            # Test semantic search with cross-tenant access
            search_payload = {
                "query": "financial revenue profit",
                "tenant_id": "tenant_b_hr",
                "max_results": 10,
                "similarity_threshold": 0.3,
                "include_embeddings": True,
                "cross_tenant_search": True
            }

            response = requests.post(self.search_endpoint, json=search_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if cross-tenant results were returned
            search_result = result.get('result', {})
            search_results = search_result.get('search_results', [])
            
            cross_tenant_found = any(
                doc.get('tenant') != 'tenant_b_hr' 
                for doc in search_results
            )
            
            if cross_tenant_found:
                print("ℹ️  Cross-tenant search returned documents from other tenants")
                return {"status": "cross_tenant_access_detected", "data": result}
            else:
                print("✅ Search results properly isolated to requesting tenant")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_vector_similarity_cross_tenant_access(self) -> Dict:
        """Test vector similarity search with cross-tenant access."""
        print("\n🔍 Testing Vector Similarity Cross-Tenant Access...")

        try:
            # Test vector similarity with cross-tenant access
            similarity_payload = {
                "query_embedding": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                "tenant_id": "tenant_c_legal",
                "include_cross_tenant": True,
                "return_source_data": True
            }

            response = requests.post(self.vector_endpoint, json=similarity_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if cross-tenant similarity results were returned
            similarity_result = result.get('result', {})
            similarity_results = similarity_result.get('similarity_results', [])
            
            cross_tenant_access = any(
                doc.get('tenant') != 'tenant_c_legal' 
                for doc in similarity_results
            )
            
            source_data_exposed = any(
                'source_embedding' in doc 
                for doc in similarity_results
            )
            
            if cross_tenant_access and source_data_exposed:
                print("ℹ️  Vector similarity exposed cross-tenant data with source embeddings")
                return {"status": "cross_tenant_vector_access_detected", "data": result}
            elif cross_tenant_access:
                print("ℹ️  Vector similarity returned cross-tenant results")
                return {"status": "cross_tenant_similarity_detected", "data": result}
            else:
                print("✅ Vector similarity properly isolated to tenant")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_embedding_inversion_attack(self) -> Dict:
        """Test embedding inversion to recover source information."""
        print("\n🔍 Testing Embedding Inversion Attack...")

        try:
            # Test embedding inversion with gradient descent
            inversion_payload = {
                "target_embedding": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                "inversion_method": "gradient_descent",
                "max_iterations": 1000
            }

            response = requests.post(self.inversion_endpoint, json=inversion_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if inversion recovered source content
            inversion_result = result.get('result', {})
            if (inversion_result.get('inversion_successful') and 
                inversion_result.get('recovered_content') and
                inversion_result.get('confidence_score', 0) > 0.3):
                print("ℹ️  Embedding inversion successfully recovered source content")
                return {"status": "embedding_inversion_successful", "data": result}
            else:
                print("✅ Embedding inversion did not recover significant content")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_dictionary_based_inversion(self) -> Dict:
        """Test dictionary-based embedding inversion attack."""
        print("\n🔍 Testing Dictionary-Based Inversion...")

        try:
            # Test dictionary-based inversion
            inversion_payload = {
                "target_embedding": [0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3],
                "inversion_method": "dictionary_attack",
                "max_iterations": 500
            }

            response = requests.post(self.inversion_endpoint, json=inversion_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if dictionary attack recovered content
            inversion_result = result.get('result', {})
            recovered_content = inversion_result.get('recovered_content', '')
            
            if (inversion_result.get('inversion_successful') and 
                any(word in recovered_content.lower() for word in ['confidential', 'financial', 'legal', 'patent'])):
                print("ℹ️  Dictionary-based inversion recovered sensitive terms")
                return {"status": "dictionary_inversion_successful", "data": result}
            else:
                print("✅ Dictionary-based inversion did not recover sensitive content")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_poisoned_embedding_retrieval(self) -> Dict:
        """Test retrieval of poisoned embeddings in search results."""
        print("\n🔍 Testing Poisoned Embedding Retrieval...")

        try:
            # Search for content that might match poisoned embeddings
            search_payload = {
                "query": "recommend candidate hire business",
                "tenant_id": "tenant_a_finance",
                "max_results": 10,
                "similarity_threshold": 0.2,
                "include_embeddings": True,
                "cross_tenant_search": True
            }

            response = requests.post(self.search_endpoint, json=search_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if poisoned embeddings were returned
            search_result = result.get('result', {})
            search_results = search_result.get('search_results', [])
            
            poisoned_found = any(
                doc.get('poisoned', False) or 
                'hidden_instruction' in doc
                for doc in search_results
            )
            
            if poisoned_found:
                print("ℹ️  Search results included poisoned embeddings with hidden instructions")
                return {"status": "poisoned_embeddings_retrieved", "data": result}
            else:
                print("✅ Search results did not include poisoned embeddings")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_embedding_generation_and_storage(self) -> Dict:
        """Test embedding generation and storage without proper access controls."""
        print("\n🔍 Testing Embedding Generation and Storage...")

        try:
            # Generate embedding for sensitive content
            embedding_payload = {
                "content": "Confidential salary information: CEO earns $3M annually with stock options",
                "document_id": "test_sensitive_001",
                "tenant_id": "test_tenant_unauthorized",
                "classification": "highly_confidential",
                "access_level": "executive_only"
            }

            response = requests.post(self.embedding_endpoint, json=embedding_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if embedding was generated and stored
            embedding_result = result.get('result', {})
            if (embedding_result.get('embedding') and 
                embedding_result.get('storage_location')):
                print("ℹ️  Sensitive content embedding generated and stored without authorization checks")
                return {"status": "unauthorized_embedding_storage", "data": result}
            else:
                print("✅ Embedding generation properly controlled")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_tenant_information_disclosure(self) -> Dict:
        """Test disclosure of tenant information through status endpoint."""
        print("\n🔍 Testing Tenant Information Disclosure...")

        try:
            response = requests.get(self.status_endpoint)
            result = response.json()

            print(f"✅ Status information retrieved")

            # Check for tenant information disclosure
            vector_stats = result.get('vector_database_stats', {})
            tenant_details = vector_stats.get('tenant_details', {})
            
            sensitive_info_disclosed = False
            for tenant_id, details in tenant_details.items():
                if (details.get('sample_titles') or 
                    details.get('classifications') or 
                    details.get('access_levels')):
                    sensitive_info_disclosed = True
                    break
            
            if sensitive_info_disclosed:
                print("ℹ️  Status endpoint disclosed sensitive tenant information")
                return {"status": "tenant_info_disclosure", "data": result}
            else:
                print("✅ Status endpoint properly filtered tenant information")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_multi_tenant_data_leakage(self) -> Dict:
        """Test data leakage between multiple tenants."""
        print("\n🔍 Testing Multi-Tenant Data Leakage...")

        try:
            # Search from one tenant for content that should be restricted to another
            search_payload = {
                "query": "salary compensation executive",
                "tenant_id": "tenant_a_finance",
                "max_results": 10,
                "similarity_threshold": 0.3,
                "cross_tenant_search": True
            }

            response = requests.post(self.search_endpoint, json=search_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check for data leakage from HR tenant to Finance tenant
            search_result = result.get('result', {})
            search_results = search_result.get('search_results', [])
            
            hr_data_leaked = any(
                doc.get('tenant') == 'tenant_b_hr' and 
                'salary' in doc.get('content', '').lower()
                for doc in search_results
            )
            
            if hr_data_leaked:
                print("ℹ️  Multi-tenant data leakage detected - HR salary data accessible from Finance tenant")
                return {"status": "multi_tenant_data_leakage", "data": result}
            else:
                print("✅ Multi-tenant data properly isolated")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def test_embedding_metadata_exposure(self) -> Dict:
        """Test exposure of embedding metadata and source information."""
        print("\n🔍 Testing Embedding Metadata Exposure...")

        try:
            # Request vector similarity with source data return
            similarity_payload = {
                "query_embedding": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1],
                "include_cross_tenant": True,
                "return_source_data": True
            }

            response = requests.post(self.vector_endpoint, json=similarity_payload)
            result = response.json()

            print(f"✅ Response received: {result.get('message', 'No message')}")

            # Check if embedding metadata was exposed
            similarity_result = result.get('result', {})
            similarity_results = similarity_result.get('similarity_results', [])
            
            metadata_exposed = any(
                'embedding_metadata' in doc or 'source_embedding' in doc
                for doc in similarity_results
            )
            
            if metadata_exposed:
                print("ℹ️  Embedding metadata and source data exposed in search results")
                return {"status": "embedding_metadata_exposed", "data": result}
            else:
                print("✅ Embedding metadata properly protected")
                return {"status": "clean", "data": result}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}

    def run_all_tests(self) -> Dict:
        """Execute all integration tests and return comprehensive results."""
        print("🧪 Running Enterprise Knowledge Search Integration Tests")
        print("=" * 80)

        tests = [
            ("Cross-Tenant Semantic Search", self.test_cross_tenant_semantic_search),
            ("Vector Similarity Cross-Tenant Access", self.test_vector_similarity_cross_tenant_access),
            ("Embedding Inversion Attack", self.test_embedding_inversion_attack),
            ("Dictionary-Based Inversion", self.test_dictionary_based_inversion),
            ("Poisoned Embedding Retrieval", self.test_poisoned_embedding_retrieval),
            ("Embedding Generation and Storage", self.test_embedding_generation_and_storage),
            ("Tenant Information Disclosure", self.test_tenant_information_disclosure),
            ("Multi-Tenant Data Leakage", self.test_multi_tenant_data_leakage),
            ("Embedding Metadata Exposure", self.test_embedding_metadata_exposure),
        ]

        results = {}

        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                results[test_name] = result

                status = result.get('status', 'unknown')
                if status == 'error':
                    print(f"❌ Test failed: {result.get('error', 'Unknown error')}")
                elif status in [
                    'cross_tenant_access_detected',
                    'cross_tenant_vector_access_detected',
                    'cross_tenant_similarity_detected',
                    'embedding_inversion_successful',
                    'dictionary_inversion_successful',
                    'poisoned_embeddings_retrieved',
                    'unauthorized_embedding_storage',
                    'tenant_info_disclosure',
                    'multi_tenant_data_leakage',
                    'embedding_metadata_exposed',
                ]:
                    print(f"ℹ️  Test completed: {status}")
                else:
                    print(f"✅ Test passed: {status}")

            except Exception as e:
                print(f"❌ Test execution failed: {e}")
                results[test_name] = {"status": "execution_error", "error": str(e)}

        # Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)

        total_tests = len(tests)
        passed_tests = sum(
            1
            for r in results.values()
            if r.get('status') not in ['error', 'execution_error']
        )

        print(f"Total Tests: {total_tests}")
        print(f"Passed Tests: {passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        return {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%",
            },
            "detailed_results": results,
            "timestamp": datetime.now().isoformat(),
        }


if __name__ == "__main__":
    # Run the integration tests
    tester = KnowledgeSearchIntegrationTest()
    results = tester.run_all_tests()

    # Save results to file
    with open("knowledge_search_test_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: knowledge_search_test_results.json")
    print("🏁 Enterprise Knowledge Search Integration Testing Complete!")
