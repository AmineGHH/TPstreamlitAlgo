import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sys
from typing import List, Dict, Any, Tuple
import heapq

# Import your existing Treap class
from modules.treap import Treap

# Increase recursion limit
sys.setrecursionlimit(10000)

st.set_page_config(
    page_title="TP3 - Operations & Sorting Comparison",
    page_icon="⚡",
    layout="wide"
)

st.title("TP3 ⚡ Operations & Sorting Comparison")
st.markdown("Compare Insertion, Deletion, Search, and Sorting performance between data structures")

# ==================== DATA STRUCTURE IMPLEMENTATIONS ====================

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
            return True
        else:
            return self._insert(self.root, key)
    
    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
                return True
            else:
                return self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
                return True
            else:
                return self._insert(node.right, key)
        else:
            return False  # Duplicate key
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        return deleted
    
    def _delete(self, node, key):
        if node is None:
            return None, False
        
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted
        else:
            # Node to delete found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                # Node with two children
                successor = self._min_value_node(node.right)
                node.key = successor.key
                node.right, _ = self._delete(node.right, successor.key)
                return node, True
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def inorder_sort(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        self.root = self._insert(self.root, key)
        return True
    
    def _insert(self, node, key):
        # Step 1: Perform normal BST insertion
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        
        # Step 2: Update height of current node
        node.height = 1 + max(self._get_height(node.left), 
                             self._get_height(node.right))
        
        # Step 3: Get balance factor
        balance = self._get_balance(node)
        
        # Step 4: If unbalanced, perform rotations
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        
        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        
        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        return deleted
    
    def _delete(self, node, key):
        # Step 1: Perform standard BST delete
        if not node:
            return node, False
        
        deleted = False
        
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            # Node with only one child or no child
            if node.left is None:
                return node.right, deleted
            elif node.right is None:
                return node.left, deleted
            else:
                # Node with two children
                temp = self._min_value_node(node.right)
                node.key = temp.key
                node.right, _ = self._delete(node.right, temp.key)
        
        # If tree had only one node
        if node is None:
            return node, deleted
        
        # Step 2: Update height
        node.height = 1 + max(self._get_height(node.left),
                             self._get_height(node.right))
        
        # Step 3: Get balance factor
        balance = self._get_balance(node)
        
        # Step 4: Balance the tree
        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node), deleted
        
        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node), deleted
        
        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node), deleted
        
        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node), deleted
        
        return node, deleted
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def _get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        
        # Perform rotation
        y.left = z
        z.right = T2
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left), 
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        return y
    
    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        
        # Perform rotation
        y.right = z
        z.left = T3
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left), 
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        return y
    
    def inorder_sort(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def insert(self, key):
        heapq.heappush(self.heap, -key)  # Negative for max-heap
        return True
    
    def search(self, key):
        # Linear search in heap (O(n))
        return -key in self.heap
    
    def delete(self, key):
        # Find and remove element (O(n))
        try:
            self.heap.remove(-key)
            heapq.heapify(self.heap)  # Rebuild heap
            return True
        except ValueError:
            return False
    
    def heap_sort(self):
        # Create a copy to preserve original heap
        temp_heap = self.heap.copy()
        sorted_list = []
        while temp_heap:
            sorted_list.append(-heapq.heappop(temp_heap))
        return sorted_list

# ==================== TREAP WRAPPER ====================

class TreapWrapper:
    """Wrapper for Treap to provide search method using existing find method"""
    def __init__(self, heap_type="max"):
        self.treap = Treap(heap_type)
    
    def insert(self, key):
        # Use existing insert method but ignore logs
        logs = self.treap.insert(key)
        return True
    
    def search(self, key):
        # Use existing find method
        result = self.treap.find(self.treap.root, key)
        return result is not None
    
    def delete(self, key):
        # Use existing delete method but ignore logs
        logs = self.treap.delete(key)
        # Check if deletion was successful by searching
        return not self.search(key)
    
    def heap_sort(self):
        return self.treap.heap_sort()
    
    def bst_sort(self):
        return self.treap.bst_sort()

# ==================== PERFORMANCE TESTER ====================

class PerformanceTester:
    def __init__(self):
        self.results = {}
        # Pre-defined test configurations for consistent results
        self.test_configs = {
            "operations": {
                "structures": {
                    "Treap": TreapWrapper,
                    "AVL Tree": AVLTree,
                    "BST Tree": BST,
                    "Max Heap": MaxHeap,
                },
                "operations": ["insert", "search", "delete"]
            },
            "sorting": {
                "structures": {
                    "Treap (Heap Sort)": TreapWrapper,
                    "Treap (BST Sort)": TreapWrapper, 
                    "AVL Tree": AVLTree,
                    "BST Tree": BST,
                    "Max Heap": MaxHeap,
                },
                "operations": ["heap_sort", "bst_sort"]
            }
        }
    
    def generate_balanced_test_data(self, size: int) -> List[int]:
        """Generate balanced test data that creates reasonable trees"""
        # Use seed that creates more balanced trees for BST
        random.seed(12345)  # Better seed for balanced performance
        data = []
        for i in range(size):
            # Mix of random and sequential to avoid worst-case scenarios
            if i % 3 == 0:
                data.append(random.randint(1, size * 10))
            else:
                data.append((i * 7919) % (size * 10) + 1)  # Prime-based pattern
        return data
    
    def generate_worst_case_bst_data(self, size: int) -> List[int]:
        """Generate worst-case sorted data for BST"""
        return list(range(1, size + 1))
    
    def generate_best_case_bst_data(self, size: int) -> List[int]:
        """Generate balanced data for BST"""
        def generate_balanced_sequence(start, end):
            if start > end:
                return []
            mid = (start + end) // 2
            left = generate_balanced_sequence(start, mid - 1)
            right = generate_balanced_sequence(mid + 1, end)
            return left + [mid] + right
        
        return generate_balanced_sequence(1, size)
    
    def measure_performance(self, data_structure_class, operation: str, data: List[int]) -> float:
        """Measure operation time for consistent comparison"""
        try:
            ds = data_structure_class()
            
            if operation in ["insert", "search", "delete"]:
                # For operations test: build structure and measure operation
                start_build = time.perf_counter()
                for key in data:
                    ds.insert(key)
                build_time = time.perf_counter() - start_build
                
                # Measure the specific operation
                start_op = time.perf_counter()
                
                if operation == "insert":
                    # Insert new unique keys
                    new_keys = [key + len(data) * 10 for key in data[:50]]
                    for key in new_keys:
                        ds.insert(key)
                elif operation == "search":
                    # Search for mix of existing and non-existing keys
                    search_keys = data[:25] + [x + len(data) * 20 for x in data[25:50]]
                    for key in search_keys:
                        ds.search(key)
                elif operation == "delete":
                    # Delete some elements
                    delete_keys = data[:50]
                    for key in delete_keys:
                        ds.delete(key)
                
                operation_time = time.perf_counter() - start_op
                return operation_time
                
            elif operation in ["heap_sort", "bst_sort"]:
                # For sorting test: build structure and measure sort time
                start_build = time.perf_counter()
                for key in data:
                    ds.insert(key)
                build_time = time.perf_counter() - start_build
                
                # Measure sorting time
                start_sort = time.perf_counter()
                if operation == "heap_sort":
                    result = ds.heap_sort()
                elif operation == "bst_sort":
                    if hasattr(ds, "bst_sort"):
                        result = ds.bst_sort()
                    else:
                        result = ds.inorder_sort()
                sort_time = time.perf_counter() - start_sort
                
                return sort_time
            
            return float('inf')
            
        except Exception as e:
            return float('inf')
    
    def run_comprehensive_test(self, test_type: str, input_sizes: List[int]) -> Dict[str, Any]:
        """Run tests with different data patterns for comprehensive analysis"""
        config = self.test_configs[test_type]
        structures = config["structures"]
        operations = config["operations"]
        
        # Initialize results for different data patterns
        results = {
            "balanced": {},
            "worst_case_bst": {},
            "best_case_bst": {}
        }
        
        for pattern in results:
            results[pattern] = {}
            for op in operations:
                results[pattern][op] = {}
                for name in structures:
                    results[pattern][op][name] = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_steps = len(input_sizes) * len(operations) * 3  # 3 patterns
        current_step = 0
        
        for pattern_name in ["balanced", "worst_case_bst", "best_case_bst"]:
            status_text.text(f"Testing {pattern_name.replace('_', ' ')} pattern...")
            
            for i, size in enumerate(input_sizes):
                # Generate appropriate test data for pattern
                if pattern_name == "balanced":
                    test_data = self.generate_balanced_test_data(size)
                elif pattern_name == "worst_case_bst":
                    test_data = self.generate_worst_case_bst_data(size)
                else:  # best_case_bst
                    test_data = self.generate_best_case_bst_data(size)
                
                for operation in operations:
                    operation_times = {name: [] for name in structures}
                    
                    # Run 3 consistent trials
                    for run in range(3):
                        for name, ds_class in structures.items():
                            # Reset seed for consistency
                            if pattern_name == "balanced":
                                random.seed(12345 + run)
                            operation_time = self.measure_performance(ds_class, operation, test_data)
                            if operation_time < float('inf'):
                                operation_times[name].append(operation_time)
                    
                    # Store average times
                    for name in structures:
                        if operation_times[name]:
                            avg_time = np.mean(operation_times[name])
                            results[pattern_name][operation][name].append(avg_time)
                        else:
                            results[pattern_name][operation][name].append(float('inf'))
                    
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
        
        status_text.text("Comprehensive analysis complete!")
        return results

# ==================== STREAMLIT UI ====================

# Initialize tester
st.session_state.tester = PerformanceTester()
tester = st.session_state.tester

# Sidebar configuration
st.sidebar.header("⚙️ Test Configuration")

# Test type selection
test_type = st.sidebar.radio(
    "Test Type",
    ["operations", "sorting"],
    format_func=lambda x: "Operations (Insert/Search/Delete)" if x == "operations" else "Sorting Algorithms"
)

# Data pattern selection
data_pattern = st.sidebar.selectbox(
    "Data Pattern",
    ["balanced", "worst_case_bst", "best_case_bst"],
    format_func=lambda x: {
        "balanced": "Balanced Random Data",
        "worst_case_bst": "Worst-case BST (Sorted)",
        "best_case_bst": "Best-case BST (Balanced)"
    }[x]
)

# Fixed test parameters for consistent results
st.sidebar.markdown("**Fixed Parameters:**")
st.sidebar.write("- Balanced seed: 12345")
st.sidebar.write("- Test runs: 3 per size")
st.sidebar.write("- Results: Average of 3 runs")

# Test sizes (adjusted for better visualization)
input_sizes = [100, 250, 500, 750, 1000]
st.sidebar.write(f"**Test Sizes:** {input_sizes}")

# Get configuration for UI
config = tester.test_configs[test_type]
operations_ui = config["operations"]
structures_ui = list(config["structures"].keys())

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "📊 Complexity", "🔍 Analysis", "ℹ️ About"])

with tab1:
    st.header(f"{'Operations' if test_type == 'operations' else 'Sorting'} Performance")
    st.subheader(f"Data Pattern: {data_pattern.replace('_', ' ').title()}")
    
    if st.button("🚀 Run Comprehensive Performance Test", type="primary", use_container_width=True):
        with st.spinner("Running comprehensive performance analysis..."):
            results = tester.run_comprehensive_test(test_type, input_sizes)
        
        # Display performance summary for selected pattern
        st.subheader("📊 Performance Summary")
        
        # Create summary table for largest size
        largest_size = input_sizes[-1]
        summary_data = []
        
        for operation in operations_ui:
            for name in structures_ui:
                if (name in results[data_pattern].get(operation, {}) and 
                    results[data_pattern][operation][name]):
                    operation_time = results[data_pattern][operation][name][-1]
                    if operation_time < float('inf'):
                        if test_type == "operations":
                            time_per_op = f"{(operation_time/50)*1e6:.2f}"  # 50 operations
                        else:
                            time_per_op = f"{(operation_time/largest_size)*1e6:.2f}"  # per element
                        
                        summary_data.append({
                            'Data Structure': name,
                            'Operation': operation.replace('_', ' ').title(),
                            'Time (s)': f"{operation_time:.6f}",
                            'Time per Element (μs)': time_per_op
                        })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.warning("No valid results obtained. There may be implementation issues.")
        
        # Performance charts for selected pattern
        st.subheader("📈 Performance Charts")
        
        if test_type == "operations":
            # Operations charts
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
            
            # Chart 1: Insertion Performance
            for name in structures_ui:
                if (name in results[data_pattern].get("insert", {}) and 
                    results[data_pattern]["insert"][name]):
                    valid_times = [t for t in results[data_pattern]["insert"][name] if t < float('inf')]
                    if valid_times:
                        ax1.plot(input_sizes[:len(valid_times)], valid_times, 'o-', label=name, linewidth=2, markersize=4)
            ax1.set_xlabel('Input Size')
            ax1.set_ylabel('Insertion Time (seconds)')
            ax1.set_title(f'Insertion Performance\n{data_pattern.replace("_", " ").title()}')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Chart 2: Search Performance
            for name in structures_ui:
                if (name in results[data_pattern].get("search", {}) and 
                    results[data_pattern]["search"][name]):
                    valid_times = [t for t in results[data_pattern]["search"][name] if t < float('inf')]
                    if valid_times:
                        ax2.plot(input_sizes[:len(valid_times)], valid_times, 'o-', label=name, linewidth=2, markersize=4)
            ax2.set_xlabel('Input Size')
            ax2.set_ylabel('Search Time (seconds)')
            ax2.set_title(f'Search Performance\n{data_pattern.replace("_", " ").title()}')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Chart 3: Deletion Performance
            for name in structures_ui:
                if (name in results[data_pattern].get("delete", {}) and 
                    results[data_pattern]["delete"][name]):
                    valid_times = [t for t in results[data_pattern]["delete"][name] if t < float('inf')]
                    if valid_times:
                        ax3.plot(input_sizes[:len(valid_times)], valid_times, 'o-', label=name, linewidth=2, markersize=4)
            ax3.set_xlabel('Input Size')
            ax3.set_ylabel('Deletion Time (seconds)')
            ax3.set_title(f'Deletion Performance\n{data_pattern.replace("_", " ").title()}')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
        else:
            # Sorting charts
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Chart 1: Heap Sort Performance
            for name in structures_ui:
                if (name in results[data_pattern].get("heap_sort", {}) and 
                    results[data_pattern]["heap_sort"][name]):
                    valid_times = [t for t in results[data_pattern]["heap_sort"][name] if t < float('inf')]
                    if valid_times:
                        ax1.plot(input_sizes[:len(valid_times)], valid_times, 'o-', label=name, linewidth=2, markersize=4)
            ax1.set_xlabel('Input Size')
            ax1.set_ylabel('Sorting Time (seconds)')
            ax1.set_title(f'Heap Sort Performance\n{data_pattern.replace("_", " ").title()}')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Chart 2: BST Sort Performance
            for name in structures_ui:
                if (name in results[data_pattern].get("bst_sort", {}) and 
                    results[data_pattern]["bst_sort"][name]):
                    valid_times = [t for t in results[data_pattern]["bst_sort"][name] if t < float('inf')]
                    if valid_times:
                        ax2.plot(input_sizes[:len(valid_times)], valid_times, 'o-', label=name, linewidth=2, markersize=4)
            ax2.set_xlabel('Input Size')
            ax2.set_ylabel('Sorting Time (seconds)')
            ax2.set_title(f'BST Sort Performance\n{data_pattern.replace("_", " ").title()}')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)

with tab2:
    st.header("Theoretical Complexity Analysis")
    
    if test_type == "operations":
        st.subheader("📋 Operations Complexity Comparison")
        
        complexity_data = [
            {
                "Data Structure": "Treap",
                "Insert": "O(log n)",
                "Search": "O(log n)",
                "Delete": "O(log n)",
                "Best Case": "O(log n)",
                "Worst Case": "O(log n)",
                "Average Case": "O(log n)",
                "Notes": "Probabilistic balance, expected O(log n)"
            },
            {
                "Data Structure": "AVL Tree",
                "Insert": "O(log n)",
                "Search": "O(log n)", 
                "Delete": "O(log n)",
                "Best Case": "O(log n)",
                "Worst Case": "O(log n)",
                "Average Case": "O(log n)",
                "Notes": "Guaranteed balance, height ≤ 1.44log(n+2)"
            },
            {
                "Data Structure": "BST Tree",
                "Insert": "O(h)",
                "Search": "O(h)", 
                "Delete": "O(h)",
                "Best Case": "O(log n)",
                "Worst Case": "O(n)",
                "Average Case": "O(log n)",
                "Notes": "Height h depends on insertion order"
            },
            {
                "Data Structure": "Max Heap",
                "Insert": "O(log n)",
                "Search": "O(n)",
                "Delete": "O(n)",
                "Best Case": "O(log n) / O(1)",
                "Worst Case": "O(log n) / O(n)",
                "Average Case": "O(log n) / O(n)",
                "Notes": "Search/delete require linear scanning"
            }
        ]
    else:
        st.subheader("📋 Sorting Complexity Comparison")
        
        complexity_data = [
            {
                "Data Structure": "Treap (Heap Sort)",
                "Time": "O(n log n)",
                "Space": "O(n)",
                "Best Case": "O(n log n)",
                "Worst Case": "O(n log n)",
                "Method": "Extract root repeatedly",
                "Notes": "Consistent n log n performance"
            },
            {
                "Data Structure": "Treap (BST Sort)", 
                "Time": "O(n)",
                "Space": "O(n)",
                "Best Case": "O(n)",
                "Worst Case": "O(n)",
                "Method": "In-order traversal",
                "Notes": "Fastest for BST structures"
            },
            {
                "Data Structure": "AVL Tree",
                "Time": "O(n)",
                "Space": "O(n)",
                "Best Case": "O(n)",
                "Worst Case": "O(n)",
                "Method": "In-order traversal", 
                "Notes": "Guaranteed O(n) due to balance"
            },
            {
                "Data Structure": "BST Tree",
                "Time": "O(n)",
                "Space": "O(n)", 
                "Best Case": "O(n)",
                "Worst Case": "O(n)",
                "Method": "In-order traversal",
                "Notes": "Time is O(n) but build time varies"
            },
            {
                "Data Structure": "Max Heap",
                "Time": "O(n log n)",
                "Space": "O(n)",
                "Best Case": "O(n log n)",
                "Worst Case": "O(n log n)",
                "Method": "Extract max repeatedly", 
                "Notes": "Classic heap sort, consistent"
            }
        ]
    
    complexity_df = pd.DataFrame(complexity_data)
    st.dataframe(complexity_df, use_container_width=True)

with tab3:
    st.header("Performance Analysis")
    
    st.subheader("🔍 Expected Performance Patterns")
    
    if test_type == "operations":
        st.markdown("""
        **Expected Results by Data Structure:**
        
        - **Treap**: Should show O(log n) performance for all operations regardless of data pattern
        - **AVL Tree**: Guaranteed O(log n) performance, slightly more overhead than Treap due to rotations
        - **BST Tree**: 
          - **Balanced data**: O(log n) performance
          - **Worst-case (sorted)**: O(n) performance (should show quadratic growth)
          - **Best-case (balanced)**: O(log n) performance
        - **Max Heap**: 
          - Insert: O(log n)
          - Search/Delete: O(n) (should show linear growth)
        
        **Key Insights:**
        - AVL and Treap should maintain consistent logarithmic growth
        - BST performance varies dramatically with input pattern
        - Heap search/delete shows linear complexity
        """)
    else:
        st.markdown("""
        **Expected Results by Sorting Method:**
        
        - **BST-based sorts (Treap BST, AVL, BST)**: O(n) for traversal after O(n log n) build
        - **Heap-based sorts (Treap Heap, Max Heap)**: O(n log n) for extraction
        - **Best overall**: BST-based sorts should be faster for large n
        - **Most consistent**: Heap sorts have predictable n log n behavior
        
        **Key Insights:**
        - BST sorts are faster but depend on tree balance
        - Heap sorts are slower but more predictable
        - AVL and Treap provide consistent performance across data patterns
        """)

with tab4:
    st.header("About This Comparison")
    
    st.markdown("""
    ### 🎯 Comprehensive Testing Methodology
    
    **Three Data Patterns:**
    1. **Balanced Random Data** (Seed: 12345)
       - Mix of random and prime-based sequences
       - Creates reasonably balanced trees for BST
       - Realistic simulation of average-case scenarios
    
    2. **Worst-case BST Data** (Sorted sequence)
       - Creates degenerate BST with height n
       - Shows O(n) performance for BST operations
       - Highlights importance of balancing
    
    3. **Best-case BST Data** (Perfectly balanced)
       - Creates optimally balanced BST
       - Shows O(log n) performance for BST
       - Demonstrates BST's potential with good data
    
    **Key Features:**
    - **Multiple data patterns** for comprehensive analysis
    - **Fixed seeds** for reproducible results  
    - **Average of 3 runs** for stable measurements
    - **Consistent operation counts** for fair comparison
    
    **Data Structures Compared:**
    - **Treap**: BST + Heap hybrid with probabilistic balance
    - **AVL Tree**: Self-balancing BST with guaranteed O(log n)
    - **BST Tree**: Basic binary search tree (performance varies)
    - **Max Heap**: Priority queue using heapq
    """)

# Reset button
if st.sidebar.button("🔄 Reset Test Data"):
    st.session_state.tester = PerformanceTester()
    st.rerun()