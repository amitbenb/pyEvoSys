import os
import datetime

time_stamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
out_path = 'output_' + time_stamp + "/"
print(out_path)

if not os.path.exists(out_path):
    os.makedirs(out_path)

experiment_big_fit_out_file_name = out_path + 'big_fit_out.txt'

solution_file_name = out_path + 'solutions'

number_of_simulations = 1

