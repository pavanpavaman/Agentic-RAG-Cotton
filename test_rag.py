"""
Test RAG System with 20 Questions about Cotton Pest and Disease Management
This script tests the RAG system with diverse questions and evaluates the answers
"""
import os
import json
from datetime import datetime
from rag_qa import answer_question
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 20 Test Questions about Cotton Pest and Disease Management
TEST_QUESTIONS = [
    # General Management Questions
    "What are the main pests affecting cotton crops?",
    "What are the common diseases found in cotton plants?",
    "What is the recommended integrated pest management strategy for cotton?",
    "How can farmers identify early signs of pest infestation in cotton?",
    
    # Specific Pest Questions
    "What is the life cycle of cotton bollworm?",
    "How to control whitefly in cotton crops?",
    "What are the symptoms of pink bollworm infestation?",
    "What is the best time to spray pesticides for controlling cotton pests?",
    
    # Disease Questions
    "What causes cotton leaf curl disease?",
    "How to prevent wilt disease in cotton?",
    "What are the symptoms of bacterial blight in cotton?",
    "How to manage root rot in cotton plants?",
    
    # Treatment and Control Questions
    "What are the recommended chemical pesticides for cotton pest control?",
    "What biological control methods are effective for cotton pests?",
    "What is the recommended dosage for pest control in cotton?",
    "How often should cotton fields be monitored for pests?",
    
    # Preventive Measures
    "What preventive measures can reduce pest infestation in cotton?",
    "What crop rotation practices help in cotton pest management?",
    "How does weather affect pest occurrence in cotton?",
    "What are the best agricultural practices to minimize cotton diseases?"
]

def run_test_suite():
    """Run all test questions and save results"""
    print("=" * 80)
    print("COTTON RAG SYSTEM - TEST SUITE")
    print("=" * 80)
    print(f"Total Questions: {len(TEST_QUESTIONS)}")
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    results = []
    
    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n{'=' * 80}")
        print(f"Question {i}/{len(TEST_QUESTIONS)}")
        print(f"{'=' * 80}")
        print(f"Q: {question}")
        print(f"{'-' * 80}")
        
        try:
            answer = answer_question(question)
            print(f"A: {answer}")
            
            # Analyze answer quality
            has_citation = "[Source p." in answer
            answer_length = len(answer)
            word_count = len(answer.split())
            
            result = {
                "question_num": i,
                "question": question,
                "answer": answer,
                "has_citation": has_citation,
                "answer_length": answer_length,
                "word_count": word_count,
                "status": "success"
            }
            
            print(f"\n✓ Citations: {'Yes' if has_citation else 'No'}")
            print(f"✓ Length: {word_count} words")
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            result = {
                "question_num": i,
                "question": question,
                "answer": None,
                "error": str(e),
                "status": "error"
            }
        
        results.append(result)
        print(f"{'=' * 80}\n")
    
    return results

def analyze_results(results):
    """Analyze and print summary statistics"""
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    total = len(results)
    successful = len([r for r in results if r['status'] == 'success'])
    with_citations = len([r for r in results if r.get('has_citation', False)])
    errors = len([r for r in results if r['status'] == 'error'])
    
    avg_word_count = sum([r.get('word_count', 0) for r in results]) / total if total > 0 else 0
    
    print(f"\nTotal Questions: {total}")
    print(f"Successful Answers: {successful} ({successful/total*100:.1f}%)")
    print(f"Answers with Citations: {with_citations} ({with_citations/total*100:.1f}%)")
    print(f"Errors: {errors}")
    print(f"Average Answer Length: {avg_word_count:.1f} words")
    
    print("\n" + "-" * 80)
    print("QUALITY ASSESSMENT")
    print("-" * 80)
    
    if with_citations >= total * 0.9:
        print("✓ EXCELLENT: >90% answers have source citations")
    elif with_citations >= total * 0.7:
        print("✓ GOOD: 70-90% answers have source citations")
    else:
        print("⚠ NEEDS IMPROVEMENT: <70% answers have source citations")
    
    if successful == total:
        print("✓ EXCELLENT: All questions answered successfully")
    elif successful >= total * 0.9:
        print("✓ GOOD: >90% questions answered successfully")
    else:
        print("⚠ NEEDS IMPROVEMENT: Some questions failed")
    
    print("\n" + "-" * 80)
    print("CITATION ANALYSIS")
    print("-" * 80)
    
    questions_without_citations = [r for r in results if r['status'] == 'success' and not r.get('has_citation', False)]
    if questions_without_citations:
        print(f"\n⚠ Questions without citations ({len(questions_without_citations)}):")
        for r in questions_without_citations:
            print(f"  - Q{r['question_num']}: {r['question'][:60]}...")
    else:
        print("\n✓ All successful answers include citations!")
    
    print("\n" + "=" * 80)

def save_results(results):
    """Save results to JSON file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_results_{timestamp}.json"
    
    output = {
        "test_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_questions": len(results),
        "results": results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {filename}")
    return filename

if __name__ == "__main__":
    try:
        # Run test suite
        results = run_test_suite()
        
        # Analyze results
        analyze_results(results)
        
        # Save results
        save_results(results)
        
        print("\n" + "=" * 80)
        print("TEST SUITE COMPLETED")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
