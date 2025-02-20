import json

def find_coverage_gaps(offsets, array_length):
    """
    Analyzes coverage of array indices based on pairs of offsets.
    Returns tuple of (uncovered ranges, overlapping ranges)
    
    Args:
        offsets: List of tuples (start, end) representing index ranges
        array_length: Length of the array being indexed into
        
    Returns:
        (list of uncovered ranges, list of overlapping ranges)
    """
    # Create array to track coverage count
    coverage = [0] * array_length
    
    # Mark coverage for each range
    for start, end in offsets:
        for i in range(start, end):
            coverage[i] += 1
    
    # Find gaps (zeros) and overlaps (>1)
    gaps = []
    overlaps = []
    gap_start = None
    overlap_start = None
    
    for i in range(array_length):
        # Handle gaps
        if coverage[i] == 0:
            if gap_start is None:
                gap_start = i
        elif gap_start is not None:
            gaps.append((gap_start, i))
            gap_start = None
            
        # Handle overlaps
        if coverage[i] > 1:
            if overlap_start is None:
                overlap_start = i
        elif overlap_start is not None:
            overlaps.append((overlap_start, i))
            overlap_start = None
    
    # Handle ranges that extend to the end
    if gap_start is not None:
        gaps.append((gap_start, array_length))
    if overlap_start is not None:
        overlaps.append((overlap_start, array_length))
        
    return gaps, overlaps

def main():
    with open("6993_errors.json", 'r') as file:
        errors_dump = json.load(file)
    sections = errors_dump["chunk_data"]
    transcript = errors_dump["transcript"]
    numlines = transcript.count("\n")
    ranges = []
    for section in sections:
        ranges.extend((section["start_idx"], section["end_idx"]))
    gaps, overlaps = find_coverage_gaps(ranges, numlines)
    print(gaps)
    print(overlaps)

main()
