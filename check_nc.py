# Program to check .nc files and inspect variables
# Date: 2025-may-14
# Version: 0.2.0

import numpy as np
import xarray as xr
import argparse
import os
from netCDF4 import Dataset

def verificar_arquivo_corrompido(caminho_arquivo):
    try:
        # Try open .nc file in read-only mode
        dataset = Dataset(caminho_arquivo, 'r')
        
        # Its ok the file isn't corrupted
        print(f"\n O arquivo '{caminho_arquivo}' foi aberto com sucesso.")
        dataset.close()
        return False  # isn't corrupted
    except Exception as e:
        # Its not ok file is corrutped or read problem
        print(f"\n Erro ao tentar abrir o arquivo '{caminho_arquivo}': {e}")
        return True  # is corrupted

def listar_variaveis(caminho_arquivo, nome_variavel=None, minmax=False):
    try:
        # Open .nc file in read-only mode
        dataset = Dataset(caminho_arquivo, 'r')

        numero_variaveis = len(dataset.variables)
        print(f"\n Arquivo NetCDF: {caminho_arquivo}")
        print("\n Dimensões disponíveis:")
        for dim in dataset.dimensions:
            print(f"  - {dim}: {len(dataset.dimensions[dim])}")
        
        print(f"\n Número total de variáveis no arquivo: {numero_variaveis}")
        print("\n Variáveis disponíveis:")
        for var in dataset.variables:
            print(f"  - {var} (dimensões: {dataset.variables[var].dimensions})")
        
        if nome_variavel:
            # Variable exists
            if nome_variavel in dataset.variables:
                print(f"\n Detalhes da variável '{nome_variavel}':")
                var = dataset.variables[nome_variavel]
                print(f"  Dimensões: {var.dimensions}")
                print(f"  Forma: {var.shape}")
                print(f"  Atributos: {var.ncattrs()}")
                for attr in var.ncattrs():
                    print(f"    {attr}: {getattr(var, attr)}")
                
                if minmax:
                    #Imprimir min e maximos
                    dados = var[:]  # Carrega os dados da variável como array numpy
                    min_val = np.min(dados)
                    max_val = np.max(dados)
                    idx_min = np.unravel_index(np.argmin(dados), dados.shape)
                    idx_max = np.unravel_index(np.argmax(dados), dados.shape)
                    print(f" \n Valor mínimo: {min_val}")
                    print(f"  Índice mínimo: {idx_min}")
                    print(f"  Coordenadas do mínimo:")
                    for i, dim in enumerate(var.dimensions):
                        valor_coord = dataset.variables[dim][idx_min[i]]
                        print(f"    {dim}: {valor_coord}")

                    print(f"\n  Valor máximo: {max_val}")
                    print(f"  Índice máximo: {idx_max}")
                    print(f"  Coordenadas do máximo:")
                    for i, dim in enumerate(var.dimensions):
                        valor_coord = dataset.variables[dim][idx_max[i]]
                        print(f"    {dim}: {valor_coord}")
 
                # Exibição de valores ajustada para diferentes dimensões
                try:
                    # Obtém a forma da variável
                    shape = dataset.variables[nome_variavel].shape
                    ndim = len(shape)  # Número de dimensões
                    print("\n  Valores:")
                    if ndim == 1:  # Variável 1D
                        print(f"    Prévia 1D (5 primeiros valores):\n {dataset.variables[nome_variavel][:5]}")
                    elif ndim == 2:  # Variável 2D
                        print(f"    Prévia 2D (5x5):\n{dataset.variables[nome_variavel][:5, :5]}")
                    elif ndim == 3:  # Variável 3D
                        print(f"    Prévia 3D (5x5x5):\n{dataset.variables[nome_variavel][:5, :5, :5]}")
                    else:  # Dimensões superiores
                        print(f"    Prévia 4D > (5x5x5x5...):\n{dataset.variables[nome_variavel][:5, :5, :5, :5]}")
                except Exception as e:
                        print(f"\n  Não foi possível carregar os valores da variável: {e}")
            elif nome_variavel=="ALL":
                # Case off --variable
                print("\n----- Você selecionou 'ALL' or 'none' mostrando cabeçalho de atributos de todas as variaveis -----")
                print("\n Detalhes das variáveis:")
                for var in dataset.variables:
                    print(f"\n Variável: {var}")
                    print(f"  Dimensões: {dataset.variables[var].dimensions}")
                    print(f"  Forma: {dataset.variables[var].shape}")
                    print(f"  Atributos: {dataset.variables[var].ncattrs()}")
                    for attr in dataset.variables[var].ncattrs():
                        print(f"    {attr}: {getattr(dataset.variables[var], attr)}")
            else:
                print(f"\n A variável '{nome_variavel}' não existe no arquivo.")

        # Close NetCDF file
        dataset.close()
    except Exception as e:
        print(f"\n Erro ao processar o arquivo: {e}")

def listar_variaveis_xarray(caminho_arquivo, nome_variavel=None):
    # Carregar o arquivo NetCDF
    ds = xr.open_dataset(caminho_arquivo)

    # Verificar as variáveis disponíveis
    print(ds)

    if nome_variavel is None:
        # Se nenhuma variável foi passada, lista todas
        print("\n Variáveis disponíveis no arquivo:")
        print(list(ds.data_vars))
        return

    # Verificar se a variável existe no dataset
    if nome_variavel not in ds.data_vars:
        print(f"\n Erro: a variável '{nome_variavel}' não existe no arquivo.")
        print(" Variáveis disponíveis:", list(ds.data_vars))
        return

    # Verificar os valores mínimo e máximo da variável
    min_val = ds[nome_variavel].min().values
    max_val = ds[nome_variavel].max().values

    print(f"\n Variavel: '{nome_variavel}'")
    print(f"\n Valor mínimo: {min_val}")
    print(f" Valor máximo: {max_val}")

if __name__ == "__main__":
    # Arguments config
    parser = argparse.ArgumentParser(description="Check de integridade, inspecionar uma variável específica ou todas em um arquivo NetCDF.")
    parser.add_argument("arquivos", nargs='+', help="Caminhos para os arquivos .nc")
    parser.add_argument("--var", nargs="?", const="ALL", help="Nome da variável para inspecionar")
    parser.add_argument("--minmax", action="store_true", help="Verifica os valores minimos e máximos da variável forneceida", default=None)
    parser.add_argument("--xarray", action="store_true", help="Verifica os valores minimos e máximos da variável forneceida por xarray - necessário --minmax ativo e --var", default=None)
    parser.add_argument("--check",action="store_true", help="Testar apenas a leitura do arquivo")
    args = parser.parse_args()

    for caminho_arquivo in args.arquivos:
        # File found or not found
        if not os.path.isfile(caminho_arquivo):
            print(f"\nErro: O arquivo '{args.arquivo}' não foi encontrado.")
        else:
            # Caminho para o arquivo NetCDF
            if args.check:
                if verificar_arquivo_corrompido(caminho_arquivo):
                    print("\n O arquivo está corrompido.\n\n")
                else:
                    print("\n O arquivo está válido.\n\n")
            elif args.var and not args.xarray:
                listar_variaveis(caminho_arquivo, args.var, args.minmax)
            elif args.xarray and args.minmax and args.var:
                listar_variaveis_xarray(caminho_arquivo, args.var)
            else:
                print("\n\n Use -h para help\n\n")
