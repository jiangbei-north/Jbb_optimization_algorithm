import numpy as np
import matplotlib.pyplot as plt
import math
import random
import os
'''
初始化种群坐标
'''
def InitialPositions(populationSize, xmin, xmax, iterations, obj_func):
    #变量维度
    dimensions = len(xmin)

    #使用numpy初始化全体坐标为0
    
    pos = np.zeros((populationSize, dimensions))

    #随机初始化种群坐标
    for i in range(populationSize):
        for j in range(dimensions):
            
             
            pos[i,j] = random.uniform(xmin[j], xmax[j])
            
               
        #  生成的第i个可变坐标的目标函数值，并将其存储在最后一列
        
        pos[i,-1] = obj_func(pos[i,0:-1])
    

    #print(pos)    
    return pos
   
'''
初始化食物位置
'''
def InitialFood(dimensions, obj_func):
    
    # 初始化食物位置为0
    
    fpos = np.zeros((1, dimensions+1))
    
    # 为所有维度赋值（最后一列除外）
    for j in range(dimensions):
        fpos[0,j] = 0.0
        
    # 计算该坐标的目标值
    fpos[0,-1] = obj_func(fpos[0,0:-1])
    
    return fpos

'''
更新食物位置
'''
def updateFood(pos, fpos):
    
    for i in range(pos.shape[0]):
        
        if (fpos[0,-1] > pos[i,-1]):
            
            # 使用樽海鞘坐标更新食物坐标
            for j in range(pos.shape[1]):
                fpos[0,j] = pos[i,j]
    return fpos

'''
更新樽海鞘位置
'''
def update_position(pos, fpos, c1, xmin, xmax, obj_func):
    
    
    # 樽海鞘种群规模
    n = len(pos[0])
    
    # 变量维度
    dimensions = len(xmin)
    
    #开始更新坐标
    
    for i in range(n):
        
        if(i<=n/2):
            
            
            #更新第i个变量的维度
            
            for j in range(dimensions):
                
                
                # 随机生成c2、c3
                c2 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                c3 = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                
                if (c3 >= 0.5):
                    
                    # 这里的clip函数用于映射搜索空间之外的坐标
                    
                    pos[i,j] = np.clip((fpos[0,j] + c1*((xmax[j] - xmin[j])*c2 + xmin[j])), xmin[j], xmax[j])
                else:
                    
                    pos[i,j] = np.clip((fpos[0,j] - c1*((xmax[j] - xmin[j])*c2 + xmin[j])), xmin[j], xmax[j])
                    
            
            
        elif(i > n/2 and i < n + 1):
            
            for j in range(dimensions):
                
                # 第i个和第i-1个变量坐标的平均值
                pos[i,j] = np.clip(((pos[i - 1,j] + pos[i,j])/2), xmin[j], xmax[j]) 
                
                
        # 计算此更新坐标的目标值
        pos[i,-1] = obj_func(pos[i,0:-1])         
    return pos


def ssa(populationSize, xmin, xmax, iterations, obj_func):
    
    L = iterations
    # 变量维度
    dimensions = len(xmin) 
    
    # 初始化
    pos  =  InitialPositions(populationSize, xmin, xmax, iterations, obj_func)
    
    


    # 初始化当前全局最优的食物位置
    fpos =  InitialFood(dimensions, obj_func)
    #print("初始食物：{}",fpos)
    

    # 1.确定画布
    plt.figure(figsize=(8, 4))
    # 迭代
    for l in range(L): 
        plt.cla()
        for i in range(len(pos)):  # shape[] 类别的种类数量(2)
           #print(pos[i])
           plt.scatter(pos[i][0],pos[i][1])  
        # 3.展示图形
        plt.pause(0.2)
        
        
        # 每次迭代后打印最佳位置
        #print("Generation ={} f(x) = {}".format(l, fpos[0-1]))
        
        
        # 更新c1  c1:是一个随着算法迭代逐渐减小的值（动态更新步长）
        c1 = 2*math.exp(-(4*(l/L))**2)
        
        
        # 更新食物位置
        fpos = updateFood(pos, fpos)
        
        # 更新樽海鞘位置
        
        pos = update_position(pos, fpos, c1, xmin, xmax, obj_func) 
        
    
        

    # plt.show()  # 显示图片
         
        
    
    
    # 打印最终食物位置
    print(fpos)
    
    return pos

# 基准函数测试
def sphereModel(variables_values = [0,0]):
    func_value = 0
    
    for i in range(len(variables_values)):
        func_value += variables_values[i]**2
    return func_value

f1 = ssa(populationSize = 15, xmin = [-10,-10], xmax = [10,10], iterations = 100, obj_func = sphereModel)
