from bujji_algorithms.heaps import *


def test_min_heap():
    print("\nTesting MinHeap...")
    h = MinHeap()

    # Test empty heap
    try:
        h.peek_min()
    except IndexError as e:
        print("  ✅ Empty peek_min raised:", e)

    # Insert elements
    for num in [5, 3, 8, 1, 4]:
        h.insert(num)
        print(f"  Inserted {num}, heap={h.to_list()}")

    # Extract min
    extracted = [h.extract_min() for _ in range(len(h.to_list()))]
    assert extracted == sorted(extracted), "❌ MinHeap did not extract in sorted order"
    print("  ✅ Extraction order:", extracted)

    # Build from list
    h.build_heap([7, 2, 9, 4])
    print("  Built heap from list:", h.to_list())
    assert h.extract_min() == 2, "❌ MinHeap build_heap failed"


def test_max_heap():
    print("\nTesting MaxHeap...")
    h = MaxHeap()

    try:
        h.peek_max()
    except IndexError as e:
        print("  ✅ Empty peek_max raised:", e)

    for num in [5, 3, 8, 1, 4]:
        h.insert(num)
        print(f"  Inserted {num}, heap={h.to_list()}")

    extracted = [h.extract_max() for _ in range(len(h.to_list()))]
    assert extracted == sorted(extracted, reverse=True), "❌ MaxHeap did not extract in reverse sorted order"
    print("  ✅ Extraction order:", extracted)

    h.build_heap([7, 2, 9, 4])
    print("  Built heap from list:", h.to_list())
    assert h.extract_max() == 9, "❌ MaxHeap build_heap failed"


def test_dary_heap():
    print("\nTesting DAryHeap (3-ary)...")
    h = DAryHeap(d=3)

    try:
        h.peek()
    except IndexError as e:
        print("  ✅ Empty peek raised:", e)

    for num in [10, 4, 15, 2, 8, 6]:
        h.insert(num)
        print(f"  Inserted {num}, heap={h.to_list()}")

    extracted = [h.extract_min() for _ in range(len(h.to_list()))]
    assert extracted == sorted(extracted), "❌ DAryHeap did not extract in sorted order"
    print("  ✅ Extraction order:", extracted)

    h.build_heap([12, 5, 20, 3, 9])
    print("  Built heap from list:", h.to_list())
    assert h.extract_min() == 3, "❌ DAryHeap build_heap failed"


def run_all_tests():
    test_min_heap()
    test_max_heap()
    test_dary_heap()
    print("\n🎯 All heap tests passed!")


if __name__ == "__main__":
    run_all_tests()
