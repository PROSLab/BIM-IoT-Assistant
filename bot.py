import streamlit as st

from agent import generate_response
import time
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import statistics
from datetime import datetime
import json
import matplotlib.pyplot as plt

import pathlib

def ensure_profile_runs_folder():
    """Create profile_runs folder if it doesn't exist"""
    profile_runs_path = pathlib.Path("profile_runs")
    profile_runs_path.mkdir(exist_ok=True)
    return profile_runs_path



def plot_evaluation_results(results: Dict, profile_runs_path: pathlib.Path):
    """
    Plot the evaluation results.

    Args:
        profile_runs_path:
        results: Dictionary containing evaluation results
    """
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Plot execution times
    times = results['execution_times']['all_times']
    ax1.plot(range(1, len(times) + 1), times, 'bo-')
    ax1.set_title(f"Input: {results["input_message"]}")
    ax1.set_xlabel('Run Number')
    ax1.set_ylabel('Execution Time (seconds)')

    # Plot similarity matrix heatmap
    im = ax2.imshow(results['response_similarity']['similarity_matrix'])
    ax2.set_title('Response Similarity Matrix')
    plt.colorbar(im, ax=ax2)

    plt.tight_layout()

    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = profile_runs_path / f'evaluation_plots_{timestamp}.png'
    plt.savefig(filename)
    plt.close()

def evaluate_response_consistency(message: str, n_runs: int = 5) -> Dict:
    """
    Evaluate the consistency of generate_response function by running it multiple times
    and comparing the responses.
    
    Args:
        message: Input message to test
        n_runs: Number of times to run the function
    
    Returns:
        Dictionary containing evaluation metrics
    """

    # Create profile_runs folder
    profile_runs_path = ensure_profile_runs_folder()

    # Lists to store results
    responses = []
    execution_times = []

    # Run the function n times
    print(f"Starting evaluation with {n_runs} runs...")
    for i in range(n_runs):
        print(f"\nRun {i+1}/{n_runs}")
        
        # Measure execution time
        start_time = time.time()
        response = generate_response(message)
        end_time = time.time()
        
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        responses.append(response)
        
        print(f"Execution time: {execution_time:.2f} seconds")

    # Calculate similarity matrix
    vectorizer = TfidfVectorizer().fit_transform(responses)
    similarity_matrix = cosine_similarity(vectorizer)
    
    # Calculate average similarity (excluding self-similarity)
    n = len(responses)
    total_similarity = 0
    comparison_count = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            total_similarity += similarity_matrix[i][j]
            comparison_count += 1
    
    avg_similarity = total_similarity / comparison_count if comparison_count > 0 else 1.0

    # Prepare results
    results = {
        "timestamp": datetime.now().isoformat(),
        "input_message": message,
        "number_of_runs": n_runs,
        "execution_times": {
            "mean": statistics.mean(execution_times),
            "median": statistics.median(execution_times),
            "std_dev": statistics.stdev(execution_times) if n_runs > 1 else 0,
            "min": min(execution_times),
            "max": max(execution_times),
            "all_times": execution_times
        },
        "response_similarity": {
            "average_similarity": float(avg_similarity),
            "similarity_matrix": similarity_matrix.tolist()
        },
        "responses": responses
    }
    
    # Print summary
    print("\nEvaluation Summary:")
    print(f"Average execution time: {results['execution_times']['mean']:.2f} seconds")
    print(f"Standard deviation: {results['execution_times']['std_dev']:.2f} seconds")
    print(f"Average response similarity: {results['response_similarity']['average_similarity']:.4f}")

    # Generate filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"response_evaluation_{timestamp}"

    # Save results to JSON file
    json_path = profile_runs_path / f"{base_filename}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)


    # Generate markdown report
    markdown_content = f"""## INPUT

    - **User Query**: {message}

    - **System A Outputs** (GraphDB-backed):
    """

    # Add each response
    for i, response in enumerate(responses, 1):
        markdown_content += f"  - A{i}: {response}\n"

    # Add execution time statistics
    markdown_content += f"""
    ## Execution Statistics
 
    - **Reference time**: {datetime.now().isoformat()}
    - **Average Time**: {results['execution_times']['mean']:.2f} seconds
    - **Median Time**: {results['execution_times']['median']:.2f} seconds
    - **Standard Deviation**: {results['execution_times']['std_dev']:.2f} seconds
    - **Min Time**: {results['execution_times']['min']:.2f} seconds
    - **Max Time**: {results['execution_times']['max']:.2f} seconds

    ## Response Similarity

    - **Average Similarity Score**: {results['response_similarity']['average_similarity']:.4f}
    """


    # Save markdown file
    md_path = profile_runs_path / f"{base_filename}.md"
    with open(md_path, 'w') as f:
        f.write(markdown_content)

    print(f"\nDetailed results saved to {json_path}")
    print(f"Markdown report saved to {md_path}")

    # Add this line after running the evaluation:
    plot_evaluation_results(results, profile_runs_path)
    
    return results

# Example usage:
# test_message = "What sensors are in Room 101?"
# results = evaluate_response_consistency(test_message, n_runs=5)

def write_message(role, content, save=True):
    """
    This is a helper function that saves a message to the
     session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the BIM and IoT Chatbot! How can I help you?"},
    ]


def handle_submit(message):
    """
    Submit handler:

    You will modify this method to talk with an LLM and provide
    context using data from knowledge graphs, databases, etc..
    """

    # Handle the response
    with st.spinner('Thinking...'):
        results = evaluate_response_consistency(message, n_runs=5)
        response = results['responses'][0]
        #response = generate_response(message)
        write_message('assistant', response)


for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)




# Get user input

if prompt := st.chat_input("What is up?"):
    write_message('user', prompt)
    handle_submit(prompt)