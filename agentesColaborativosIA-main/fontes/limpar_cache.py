#!/usr/bin/env python3
"""
Remove cache de Python
"""
import os
import shutil

cache_dir = r"C:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes\ui\__pycache__"

if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    print(f"✓ Cache removido: {cache_dir}")
else:
    print("Cache não existe")

# Também remove pycache global
for root, dirs, files in os.walk(r"C:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes"):
    if '__pycache__' in dirs:
        shutil.rmtree(os.path.join(root, '__pycache__'))
        print(f"✓ Removido: {os.path.join(root, '__pycache__')}")

print("\n✅ Cache de Python limpo completamente!")
