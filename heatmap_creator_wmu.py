#!/usr/bin/env python3
"""
Z-score Heatmap Creator
CSVファイルからz-scoreヒートマップを作成するプログラム

使用方法:
    python heatmap_creator.py input.csv [options]

必要なライブラリ:
    - pandas
    - matplotlib
    - seaborn
    - numpy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse
import sys
from pathlib import Path


def create_heatmap(csv_file, output_file=None, title=None, 
                   vmin=None, vmax=None, cmap='YlOrRd',
                   figsize=(20, 6), dpi=300, 
                   time_column='Time (s)', 
                   mouse_prefix='Mouse',
                   xtick_interval=500):
    """
    CSVファイルからヒートマップを作成する
    
    Parameters:
    -----------
    csv_file : str
        入力CSVファイルのパス
    output_file : str, optional
        出力画像ファイルのパス（指定しない場合は自動生成）
    title : str, optional
        ヒートマップのタイトル
    vmin : float, optional
        カラースケールの最小値
    vmax : float, optional
        カラースケールの最大値
    cmap : str, optional
        カラーマップ名（デフォルト: 'YlOrRd'）
    figsize : tuple, optional
        図のサイズ（幅, 高さ）
    dpi : int, optional
        解像度
    time_column : str, optional
        時間列の名前
    mouse_prefix : str, optional
        マウス列の接頭辞
    xtick_interval : int, optional
        x軸ラベルの間隔
    
    Returns:
    --------
    str : 出力ファイルのパス
    """
    
    # 日本語フォントの設定
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    
    # CSVファイルを読み込む
    print(f'CSVファイルを読み込んでいます: {csv_file}')
    df = pd.read_csv(csv_file)
    
    # マウス列を抽出
    mouse_columns = [col for col in df.columns if col.startswith(mouse_prefix)]
    
    if len(mouse_columns) == 0:
        raise ValueError(f'"{mouse_prefix}"で始まる列が見つかりません。')
    
    print(f'検出されたマウス列: {mouse_columns}')
    print(f'データ形状: {df.shape}')
    print(f'マウス数: {len(mouse_columns)}')
    
    # データを転置（マウスを行に）
    data_for_heatmap = df[mouse_columns].T
    
    # vmin, vmaxが指定されていない場合は自動計算
    if vmin is None:
        vmin = data_for_heatmap.values.min()
        print(f'自動計算されたvmin: {vmin:.4f}')
    
    if vmax is None:
        vmax = data_for_heatmap.values.max()
        print(f'自動計算されたvmax: {vmax:.4f}')
    
    # 図の作成
    fig, ax = plt.subplots(figsize=figsize)
    
    # ヒートマップを作成
    sns.heatmap(data_for_heatmap, 
                cmap=cmap,
                vmin=vmin,
                vmax=vmax,
                cbar_kws={'label': 'Z-score'},
                xticklabels=xtick_interval,
                yticklabels=mouse_columns,
                ax=ax)
    
    # タイトルと軸ラベルを設定
    if title is None:
        title = f'Z-score Heatmap (n={len(mouse_columns)})'
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlabel('Time Point Index', fontsize=12)
    ax.set_ylabel('Mouse ID', fontsize=12)
    
    # レイアウトを調整
    plt.tight_layout()
    
    # 出力ファイル名の生成
    if output_file is None:
        input_path = Path(csv_file)
        output_file = input_path.stem + '_heatmap.png'
    
    # 保存
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
    print(f'ヒートマップを保存しました: {output_file}')
    
    # メモリ解放
    plt.close()
    
    return output_file


def create_colorbar(vmin, vmax, output_file='colorbar.png', 
                   cmap='YlOrRd', orientation='vertical', dpi=300):
    """
    カラーバーのみの画像を作成する
    
    Parameters:
    -----------
    vmin : float
        カラースケールの最小値
    vmax : float
        カラースケールの最大値
    output_file : str
        出力画像ファイルのパス
    cmap : str
        カラーマップ名
    orientation : str
        'vertical' または 'horizontal'
    dpi : int
        解像度
    
    Returns:
    --------
    str : 出力ファイルのパス
    """
    
    # 日本語フォントの設定
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    
    # カラーマップの取得
    cmap_obj = plt.get_cmap(cmap)
    
    # 図のサイズを設定
    if orientation == 'vertical':
        figsize = (2, 8)
    else:
        figsize = (8, 2)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # 正規化
    import matplotlib as mpl
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    
    # カラーバーを作成
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap_obj, norm=norm, 
                                    orientation=orientation)
    
    # ラベルを設定
    cb.set_label('Z-score', fontsize=14, weight='bold')
    ax.tick_params(labelsize=12)
    
    # レイアウトを調整
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
    print(f'カラーバーを保存しました: {output_file}')
    
    plt.close()
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='CSVファイルからz-scoreヒートマップを作成します',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な使用方法
  python heatmap_creator.py data.csv
  
  # カラースケールを指定
  python heatmap_creator.py data.csv --vmin -1.7 --vmax 2.0
  
  # タイトルと出力ファイル名を指定
  python heatmap_creator.py data.csv -o output.png -t "My Heatmap"
  
  # カラーバーも作成
  python heatmap_creator.py data.csv --colorbar
        """
    )
    
    parser.add_argument('csv_file', help='入力CSVファイルのパス')
    parser.add_argument('-o', '--output', help='出力画像ファイルのパス')
    parser.add_argument('-t', '--title', help='ヒートマップのタイトル')
    parser.add_argument('--vmin', type=float, help='カラースケールの最小値')
    parser.add_argument('--vmax', type=float, help='カラースケールの最大値')
    parser.add_argument('--cmap', default='YlOrRd', 
                       help='カラーマップ名（デフォルト: YlOrRd）')
    parser.add_argument('--width', type=float, default=20, 
                       help='図の幅（デフォルト: 20）')
    parser.add_argument('--height', type=float, default=6, 
                       help='図の高さ（デフォルト: 6）')
    parser.add_argument('--dpi', type=int, default=300, 
                       help='解像度（デフォルト: 300）')
    parser.add_argument('--time-column', default='Time (s)', 
                       help='時間列の名前（デフォルト: "Time (s)"）')
    parser.add_argument('--mouse-prefix', default='Mouse', 
                       help='マウス列の接頭辞（デフォルト: "Mouse"）')
    parser.add_argument('--xtick-interval', type=int, default=500, 
                       help='x軸ラベルの間隔（デフォルト: 500）')
    parser.add_argument('--colorbar', action='store_true', 
                       help='カラーバーも作成する')
    
    args = parser.parse_args()
    
    # CSVファイルの存在確認
    if not Path(args.csv_file).exists():
        print(f'エラー: ファイルが見つかりません: {args.csv_file}', file=sys.stderr)
        sys.exit(1)
    
    try:
        # ヒートマップを作成
        output_file = create_heatmap(
            csv_file=args.csv_file,
            output_file=args.output,
            title=args.title,
            vmin=args.vmin,
            vmax=args.vmax,
            cmap=args.cmap,
            figsize=(args.width, args.height),
            dpi=args.dpi,
            time_column=args.time_column,
            mouse_prefix=args.mouse_prefix,
            xtick_interval=args.xtick_interval
        )
        
        # カラーバーを作成
        if args.colorbar:
            # vmin, vmaxを取得（指定されていない場合はデータから計算）
            if args.vmin is None or args.vmax is None:
                df = pd.read_csv(args.csv_file)
                mouse_columns = [col for col in df.columns 
                               if col.startswith(args.mouse_prefix)]
                data = df[mouse_columns].values
                vmin = args.vmin if args.vmin is not None else data.min()
                vmax = args.vmax if args.vmax is not None else data.max()
            else:
                vmin = args.vmin
                vmax = args.vmax
            
            # 出力ファイル名を生成
            output_path = Path(output_file)
            colorbar_v = output_path.stem + '_colorbar_vertical.png'
            colorbar_h = output_path.stem + '_colorbar_horizontal.png'
            
            create_colorbar(vmin, vmax, colorbar_v, args.cmap, 'vertical', args.dpi)
            create_colorbar(vmin, vmax, colorbar_h, args.cmap, 'horizontal', args.dpi)
        
        print('\n完了しました！')
        
    except Exception as e:
        print(f'エラーが発生しました: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
