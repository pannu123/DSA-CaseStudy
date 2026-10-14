import heapq
import gzip
import zipfile
from collections import Counter, deque
from pathlib import Path

CITY_MAP = {
    "Home": {"College": 4, "Market": 6},
    "College": {"Home": 4, "Hospital": 5, "Railway Station": 10},
    "Market": {"Home": 6, "Hospital": 3, "Airport": 15},
    "Hospital": {"College": 5, "Market": 3, "Railway Station": 4},
    "Railway Station": {"College": 10, "Hospital": 4, "Airport": 7},
    "Airport": {"Market": 15, "Railway Station": 7}
}


class HuffmanNode:
    def __init__(self, char=None, left=None, right=None):
        self.char = char
        self.left = left
        self.right = right


def get_city(name):
    city_lookup = {city.lower(): city for city in CITY_MAP}
    return city_lookup.get(name.strip().lower())


def display_city_map():
    print("\n========== CITY MAP (WEIGHTED GRAPH) ==========")
    for city in CITY_MAP:
        roads = ", ".join(
            f"{neighbor} ({distance} km)"
            for neighbor, distance in sorted(CITY_MAP[city].items())
        )
        print(f"{city}: {roads}")


def breadth_first_search(start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        city = queue.popleft()
        order.append(city)
        for neighbor in sorted(CITY_MAP[city]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def depth_first_search(start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        city = stack.pop()
        if city in visited:
            continue
        visited.add(city)
        order.append(city)
        for neighbor in sorted(CITY_MAP[city], reverse=True):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def dijkstra(start, destination):
    distances = {city: float("inf") for city in CITY_MAP}
    previous = {city: None for city in CITY_MAP}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_city = heapq.heappop(priority_queue)

        if current_distance != distances[current_city]:
            continue
        if current_city == destination:
            break

        for neighbor, weight in CITY_MAP[current_city].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_city
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if distances[destination] == float("inf"):
        return [], None

    route = []
    current = destination
    while current is not None:
        route.append(current)
        current = previous[current]
    route.reverse()
    return route, distances[destination]


def prim_mst(start):
    visited = {start}
    edges = []
    total_distance = 0
    priority_queue = []

    for neighbor, weight in CITY_MAP[start].items():
        heapq.heappush(priority_queue, (weight, start, neighbor))

    while priority_queue and len(visited) < len(CITY_MAP):
        weight, source, destination = heapq.heappop(priority_queue)
        if destination in visited:
            continue

        visited.add(destination)
        edges.append((source, destination, weight))
        total_distance += weight

        for neighbor, next_weight in CITY_MAP[destination].items():
            if neighbor not in visited:
                heapq.heappush(
                    priority_queue, (next_weight, destination, neighbor)
                )

    if len(visited) != len(CITY_MAP):
        return None, None

    return edges, total_distance


def build_huffman_tree(text):
    if not text:
        return None, {}

    frequencies = Counter(text)
    heap = []
    counter = 0

    for char, frequency in frequencies.items():
        heapq.heappush(heap, (frequency, counter, HuffmanNode(char=char)))
        counter += 1

    while len(heap) > 1:
        left_frequency, _, left_node = heapq.heappop(heap)
        right_frequency, _, right_node = heapq.heappop(heap)
        parent = HuffmanNode(left=left_node, right=right_node)
        heapq.heappush(
            heap,
            (left_frequency + right_frequency, counter, parent)
        )
        counter += 1

    root = heap[0][2]
    codes = {}

    def create_codes(node, prefix):
        if node.char is not None:
            codes[node.char] = prefix if prefix else "0"
            return
        create_codes(node.left, prefix + "0")
        create_codes(node.right, prefix + "1")

    create_codes(root, "")
    return root, codes


def huffman_encode_decode(text):
    if not text:
        print("No text entered. Nothing to encode.")
        return

    root, codes = build_huffman_tree(text)
    frequencies = Counter(text)
    encoded = "".join(codes[char] for char in text)

    if root.char is not None:
        decoded = root.char * len(text)
    else:
        decoded_chars = []
        current = root
        for bit in encoded:
            current = current.left if bit == "0" else current.right
            if current.char is not None:
                decoded_chars.append(current.char)
                current = root
        decoded = "".join(decoded_chars)

    print("\n========== HUFFMAN CODING RESULTS ==========")
    print(f"{'Character':<16}{'Frequency':<12}Huffman Code")
    print("-" * 42)

    for char in sorted(frequencies):
        if char == " ":
            label = "[SPACE]"
        elif char == "\n":
            label = "[NEWLINE]"
        elif char == "\t":
            label = "[TAB]"
        else:
            label = repr(char)
        print(f"{label:<16}{frequencies[char]:<12}{codes[char]}")

    original_bits = len(text.encode("utf-8")) * 8
    encoded_bits = len(encoded)
    reduction = (original_bits - encoded_bits) * 100 / original_bits if original_bits else 0

    print("-" * 42)
    print("Original text       :", repr(text))
    print("Huffman bit string  :", encoded)
    print("Decoded text        :", repr(decoded))
    print("Decoding successful :", decoded == text)
    print("Original UTF-8 bits :", original_bits)
    print("Encoded data bits   :", encoded_bits)
    print(f"Bit-count reduction : {reduction:.2f}%")
    print("Note: Code table, padding, and file headers are not included in this estimate.")


def safe_base_name(name):
    cleaned = Path(name).name.strip()
    if not cleaned:
        return "route_report"
    return Path(cleaned).stem or "route_report"


def create_compressed_files(text, base_name):
    base = safe_base_name(base_name)
    txt_path = Path(f"{base}.txt")
    gz_path = Path(f"{base}.txt.gz")
    zip_path = Path(f"{base}.zip")
    data = text.encode("utf-8")

    txt_path.write_bytes(data)

    with gzip.open(gz_path, "wb") as file:
        file.write(data)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(txt_path.name, data)

    print("\n========== FILE COMPRESSION RESULTS ==========")
    print("Original file :", txt_path.resolve())
    print("GZIP file     :", gz_path.resolve())
    print("ZIP file      :", zip_path.resolve())
    print("Original size :", txt_path.stat().st_size, "bytes")
    print("GZIP size     :", gz_path.stat().st_size, "bytes")
    print("ZIP size      :", zip_path.stat().st_size, "bytes")
    print("Files created successfully.")
    print("Note: Small files may become larger after compression because of headers.")


def decompress_file():
    path_text = input("Enter .gz or .zip file path: ").strip().strip('"')
    path = Path(path_text)

    if not path.is_file():
        print("File not found.")
        return

    try:
        if path.suffix.lower() == ".gz":
            with gzip.open(path, "rb") as source:
                data = source.read()
            output_path = path.with_name("decompressed_" + path.name[:-3])

        elif path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path, "r") as archive:
                names = archive.namelist()
                if not names:
                    print("ZIP archive is empty.")
                    return
                member = names[0]
                data = archive.read(member)
                output_path = path.with_name("decompressed_" + Path(member).name)
        else:
            print("Please provide a .gz or .zip file.")
            return

        output_path.write_bytes(data)
        print("Decompression successful.")
        print("Output file:", output_path.resolve())
        print("Decompressed size:", len(data), "bytes")

        try:
            text = data.decode("utf-8")
            print("Recovered text:", repr(text))
        except UnicodeDecodeError:
            print("The decompressed file is binary, so text preview is unavailable.")

    except (OSError, EOFError, zipfile.BadZipFile, RuntimeError) as error:
        print("Could not decompress file:", error)


def run_navigation(compress_report=False):
    print("\nAvailable locations:")
    for city in CITY_MAP:
        print("-", city)

    start = get_city(input("Enter starting location: "))
    destination = get_city(input("Enter destination: "))

    if start is None or destination is None:
        print("Invalid location. Please use a name from the list.")
        return

    route, distance = dijkstra(start, destination)

    if not route:
        print("No route found.")
        return

    print("\n========== GPS NAVIGATION RESULT ==========")
    print("Starting location :", start)
    print("Destination       :", destination)
    print("Shortest route    :", " -> ".join(route))
    print("Total distance    :", distance, "km")

    report = (
        "GPS NAVIGATION REPORT\n"
        f"Starting location: {start}\n"
        f"Destination: {destination}\n"
        f"Shortest route: {' -> '.join(route)}\n"
        f"Total distance: {distance} km\n"
    )

    if compress_report:
        huffman_encode_decode(report)
        create_compressed_files(report, "gps_route_report")


def main():
    while True:
        print("\n" + "=" * 58)
        print(" SMART CITY NAVIGATION AND FILE COMPRESSION SYSTEM")
        print("=" * 58)
        print("1. Display City Map")
        print("2. Find Shortest Route (Dijkstra)")
        print("3. Explore Map Using BFS")
        print("4. Explore Map Using DFS")
        print("5. Find Minimum Spanning Tree (Prim)")
        print("6. Huffman Encode and Decode Text")
        print("7. Create GZIP and ZIP Files from Text")
        print("8. Compress GPS Route Report (Huffman + GZIP + ZIP)")
        print("9. Decompress a GZIP or ZIP File")
        print("10. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_city_map()

        elif choice == "2":
            run_navigation()

        elif choice in ("3", "4"):
            start = get_city(input("Enter starting location: "))
            if start is None:
                print("Invalid location. Please use a name from the city list.")
            elif choice == "3":
                print("BFS traversal:", " -> ".join(breadth_first_search(start)))
            else:
                print("DFS traversal:", " -> ".join(depth_first_search(start)))

        elif choice == "5":
            start = get_city(input("Enter starting location for MST: "))
            if start is None:
                print("Invalid location.")
            else:
                edges, total = prim_mst(start)
                if edges is None:
                    print("The city graph is not connected; no single spanning tree exists.")
                else:
                    print("\n========== MINIMUM SPANNING TREE ==========")
                    for source, destination, weight in edges:
                        print(f"{source} -- {destination}: {weight} km")
                    print("Total road distance in MST:", total, "km")

        elif choice == "6":
            text = input("Enter text to encode using Huffman coding: ")
            huffman_encode_decode(text)

        elif choice == "7":
            text = input("Enter text to save and compress: ")
            name = input("Enter base file name (without extension): ").strip()
            create_compressed_files(text, name or "sample_text")

        elif choice == "8":
            run_navigation(compress_report=True)

        elif choice == "9":
            decompress_file()

        elif choice == "10":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
