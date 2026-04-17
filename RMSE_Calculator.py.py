import numpy as np

def rmse(predictions, targets):
    """
    计算均方根误差RMSE
    :param predictions: 预测值数组（numpy数组）
    :param targets: 真实值数组（numpy数组）
    :return: RMSE计算结果
    """
    # 校验输入长度一致
    if predictions.shape != targets.shape:
        raise ValueError(f"预测值与真实值长度不匹配！预测值长度：{predictions.shape[0]}，真实值长度：{targets.shape[0]}")
    # 核心RMSE计算（与你原公式完全一致）
    return np.sqrt(((predictions - targets) ** 2).mean())

if __name__ == "__main__":
    print("===== 均方根误差(RMSE)计算器 =====")
    print("输入规则：多个数值用 英文逗号/空格 分隔，例如：1.2 3.4 5.6 或 2,4,6,8")
    print("-" * 40)

    try:
        # 1. 获取用户输入
        pred_input = input("请输入预测值序列：").strip()
        target_input = input("请输入真实值序列：").strip()

        # 2. 解析输入为数值数组（兼容逗号/空格分隔）
        pred_list = [float(num) for num in pred_input.replace(',', ' ').split()]
        target_list = [float(num) for num in target_input.replace(',', ' ').split()]

        # 3. 转为numpy数组
        pred_array = np.array(pred_list)
        target_array = np.array(target_list)

        # 4. 计算并输出结果
        result = rmse(pred_array, target_array)
        print("-" * 40)
        print(f"✅ 计算完成")
        print(f"预测值序列：{pred_array}")
        print(f"真实值序列：{target_array}")
        print(f"最终RMSE结果：{result:.6f}")

    except ValueError as e:
        print(f"❌ 输入错误：{e}，请检查输入的是否为有效数字，且两组数值长度一致")
    except Exception as e:
        print(f"❌ 程序运行出错：{e}")