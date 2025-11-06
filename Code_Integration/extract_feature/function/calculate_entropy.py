import math
from collections import Counter

# 엔트로피 계산
def CalculateEntropy(data):
    # 각 바이트의 빈도 계산
    counter = Counter(data)
    total_bytes = len(data)
    
    # 엔트로피 계산
    entropy = 0.0
    for byte, count in counter.items():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)
    
    return entropy