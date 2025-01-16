# Program to check .nc files and inspect variables.
# Date: 15-january-2025.
# Version: 0.1.0

import argparse
import os
from netCDF4 import Dataset

def verificar_arquivo_corrompido(caminho_arquivo):
    try:
        # Try open .nc file in read-only mode
        dataset = Dataset(caminho_arquivo, 'r')
        
        # Its ok the file isn't corrupted
        print(f"O arquivo '{caminho_arquivo}' foi aberto com sucesso.")
        dataset.close()
        return False  # isn't corrupted
    except Exception as e:
        # Its not ok file is corrutped or read problem
        print(f"Erro ao tentar abrir o arquivo '{caminho_arquivo}': {e}")
        return True  # is corrupted

def listar_variaveis(caminho_arquivo, nome_variavel=None):
    try:
        # Open .nc file in read-only mode
        dataset = Dataset(caminho_arquivo, 'r')

        numero_variaveis = len(dataset.variables)
        print(f"\nArquivo NetCDF: {caminho_arquivo}")
        print("\nDimensões disponíveis:")
        for dim in dataset.dimensions:
            print(f"  - {dim}: {len(dataset.dimensions[dim])}")
        
        print(f"\nNúmero total de variáveis no arquivo: {numero_variaveis}")
        print("\nVariáveis disponíveis:")
        for var in dataset.variables:
            print(f"  - {var} (dimensões: {dataset.variables[var].dimensions})")
        
        if nome_variavel:
            # Variable exists
            if nome_variavel in dataset.variables:
                print(f"\nDetalhes da variável '{nome_variavel}':")
                var = dataset.variables[nome_variavel]
                print(f"  Dimensões: {var.dimensions}")
                print(f"  Forma: {var.shape}")
                print(f"  Atributos: {var.ncattrs()}")
                for attr in var.ncattrs():
                    print(f"    {attr}: {getattr(var, attr)}")
            else:
                print(f"A variável '{nome_variavel}' não existe no arquivo.")
        else:
            # Case off --variable
            print("\nDetalhes das variáveis:")
            for var in dataset.variables:
                print(f"\nVariável: {var}")
                print(f"  Dimensões: {dataset.variables[var].dimensions}")
                print(f"  Forma: {dataset.variables[var].shape}")
                print(f"  Atributos: {dataset.variables[var].ncattrs()}")
                for attr in dataset.variables[var].ncattrs():
                    print(f"    {attr}: {getattr(dataset.variables[var], attr)}")

        # Close NetCDF file
        dataset.close()
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    # Arguments config
    parser = argparse.ArgumentParser(description="Check de integridade, inspecionar uma variável específica ou todas em um arquivo NetCDF.")
    #parser.add_argument("arquivo", help="Caminho para o arquivo .nc")
    parser.add_argument("arquivos", nargs='+', help="Caminhos para os arquivos .nc")
    parser.add_argument("--var", help="Nome da variável para inspecionar", default=None)
    parser.add_argument("--check",action="store_true", help="Testar apenas a leitura do arquivo")
    args = parser.parse_args()

    for caminho_arquivo in args.arquivos:
        # File found or not found
        if not os.path.isfile(caminho_arquivo):
            print(f"Erro: O arquivo '{args.arquivo}' não foi encontrado.")
        else:
            # Caminho para o arquivo NetCDF
            if args.check:
                if verificar_arquivo_corrompido(caminho_arquivo):
                    print("O arquivo está corrompido.")
                else:
                    print("O arquivo está válido.")
            else:
                listar_variaveis(caminho_arquivo, args.var)

