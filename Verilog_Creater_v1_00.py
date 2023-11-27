# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 15:46:38 2023

@author: QC109_4
"""
import os
import re
import subprocess
from pathlib import Path

POSSIBLE_FIFO_DEPTH = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]

class Verilog_maker:
    def __init__(self):
        print('make verilog code...')
        
        self.fifo_generator_list = []
        self.dds_compiler_list = []
        self.rf_converter_list = []
        
        self.git_dir = 'C:\Jeonghyun\GIT'
        self.target_dir = 'AD9910_CODE\Verilog17\AD9910_V2_2'
        
        self.TTL_ports = ['GPIO_LED_0_LS', 'GPIO_LED_1_LS','DACIO_00','PMOD0_0_LS']
        
        self.total_ttl_num = len(self.TTL_ports)
        
        self.rto_fifo_depth = 256
        self.rto_fifo_threshold = self.rtob_fifo_depth - 8
        self.rto_fifo_data_len = 8
        self.rto_fifo_addr_len = len(bin(self.rto_fifo_depth - 1)) - 2 
        
        self.vivado_path = r"C:\Xilinx\Vivado\2017.3\bin\vivado.bat"
        self.board_path = "C:\Xilinx\Vivado\2017.3\data\boards\board_files"
        self.part_name = "xc7s50csga324-1"
        self.tcl_commands = ''
        self.do_sim = False
        self.make_bit_stream = (True and (not self.do_sim))
        
    def run_vivado_tcl(self, vivado_bat, tcl_path):
        self.vivado_executable = vivado_bat# Replace with the actual path to vivado.bat
    
        # Start Vivado in batch mode and pass the TCL commands as input
        process = subprocess.Popen([self.vivado_executable, "-mode", "batch", "-source", tcl_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, text=True)
    
        while process.poll() == None:
            out = process.stdout.readline()
            print(out, end='')
            
        # Wait for the process to complete
        stdout, stderr = process.communicate()
    
        # Print the output and error messages
        # print(stdout)
        print(stderr)
    
    def get_all_files_in_directory(self, directory,file_type):
        file_list = []
        is_filetype = False
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                for types_ in file_type:
                    if file.endswith(types_):
                        is_filetype = True
                if is_filetype:
                    file_list.append(os.path.join(root, file))
                is_filetype = False
        return file_list
    
    # Function to generate the "add_files" string for a given file
    def generate_add_files_string(self, file_path):
        return f'add_files -norecurse {{{file_path}}}\n'
    
    def generate_add_constraints_string(self, file_path):
        file_path_ = file_path.replace("\\","/")
        return f'add_files -fileset constrs_1 -norecurse {file_path_}'
    
    def generate_set_prj_string(self, folder_directory,prj_name):
        return f'set project_name \"{prj_name}\"\n' + f'set project_dir \"{folder_directory}\"\n'
    
    def generate_create_prj_string(self, part_name):
        return f'create_project ${{project_name}} ${{project_dir}}/${{project_name}} -part {part_name}\n'
    
    def generate_set_board(self, board_path, board_name):
        return f'set boardpath {{{board_path}}}\n' + 'set_param board.repoPaths [list $boardpath]\n' + f'set_property BOARD_PART {board_name} [current_project]\n'
        
    def generate_xilinx_fifo_generator(self, folder_directory, fifo_name):
        tcl_code = ''
        tcl_code += f'create_ip -dir {folder_directory} -name fifo_generator -vendor xilinx.com -library ip -version 13.2 -module_name {fifo_name}\n'
        tcl_code += f'set_property -dict [list CONFIG.Performance_Options {{First_Word_Fall_Through}}'
        tcl_code += f' CONFIG.Input_Data_Width {{8}} CONFIG.Input_Depth {{8192}}'
        tcl_code += f' CONFIG.Output_Data_Width {{8}} CONFIG.Output_Depth {{8192}}'
        tcl_code += f' CONFIG.Underflow_Flag {{true}} CONFIG.Overflow_Flag {{true}}'
        tcl_code += f' CONFIG.Data_Count_Width {{13}} CONFIG.Write_Data_Count_Width {{13}}'
        tcl_code += f' CONFIG.Read_Data_Count_Width {{13}}'
        tcl_code += f' [get_ips {fifo_name}]\n'
        
        #using '\' makes error in vivado.bat. this should be replaced in '/'
        tcl_code = tcl_code.replace("\\","/")
        
        return tcl_code
    
    def generate_rtio_fifo_generator(self, folder_directory, fifo_name):
        tcl_code = ''
        tcl_code += f'create_ip -dir {folder_directory} -name fifo_generator -vendor xilinx.com -library ip -version 13.2 -module_name {fifo_name}\n'
        tcl_code += f'set_property -dict [list CONFIG.Performance_Options {{First_Word_Fall_Through}}'
        tcl_code += f' CONFIG.Input_Data_Width {{8}} CONFIG.Input_Depth {{8192}}'
        tcl_code += f' CONFIG.Output_Data_Width {{8}} CONFIG.Output_Depth {{8192}}'
        tcl_code += f' CONFIG.Underflow_Flag {{true}} CONFIG.Overflow_Flag {{true}}'
        tcl_code += f' CONFIG.Data_Count_Width {{13}} CONFIG.Write_Data_Count_Width {{13}}'
        tcl_code += f' CONFIG.Read_Data_Count_Width {{13}}'
        tcl_code += f' [get_ips {fifo_name}]\n'
        
        #using '\' makes error in vivado.bat. this should be replaced in '/'
        tcl_code = tcl_code.replace("\\","/")
        
        return tcl_code
        
    def ensure_directory_exists(self, directory_path):
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
                print(f"Directory {directory_path} created.")
            except OSError as error:
                print(f"Error creating directory {directory_path}: {error}")
        else:
            print(f"Directory {directory_path} already exists.")
            
    def remove_duplicates_set(self, lst):
        return list(set(lst))
        
    def generate_time_controller(self, current_dir = None):
        if current_dir == None:
            source_dir = './TimeController'
        else:
            source_dir = f'{current_dir}/TimeController'
        
        full_dir = os.path.join(self.git_dir, self.time_controller_dir.lstrip('/').lstrip('\\'))
        base_dir = os.path.dirname(full_dir)
        base_name = os.path.basename(full_dir)
        new_full_dir = os.path.join(base_dir,base_name)
        new_output_full_dir =os.path.join(base_dir,base_name.lstrip('/').lstrip('\\') + '_output')
        self.ensure_directory_exists(new_full_dir)
            
        for filename in os.listdir(source_dir):
            source_path = os.path.join(source_dir, filename)
            file_root, file_extension = os.path.splitext(filename)
            new_filename = file_root + file_extension
            destination_path = os.path.join(new_full_dir, new_filename)
        
            # Open the source file and read its contents
            verilog_code = ''
            with open(source_path, 'r') as source_file:
                verilog_code = source_file.read()
                
            # Write the modified content to the destination file
            with open(destination_path, 'w') as destination_file:
                destination_file.write(verilog_code)

        self.make_time_controller_tcl(new_output_full_dir, 'TimeController', self.part_name, self.board_path, self.board_name, new_full_dir, ['.sv', '.v','.xic'])
        
    def make_time_controller_tcl(self, folder_directory,prj_name,part_name,board_path,board_name,src_folder_directory,file_type):
        file_name = prj_name+".tcl"
        print(file_name)
        # Combine the file name and folder directory to create the full file path
        file_path = folder_directory + '\\' + file_name
        print(file_path)
        
        self.ensure_directory_exists(folder_directory)
        self.ensure_directory_exists(src_folder_directory)
        #add src files
        self.set_project(folder_directory, prj_name)
        self.create_project(part_name)
        self.add_src(src_folder_directory,file_type)
        self.set_board(board_path, board_name)
        
        # Save the TCL code to the .tcl file
        
        self.tcl_commands += self.generate_customized_ip(folder_directory)
        
        self.tcl_commands += f'set_property top TimeController [current_fileset]\n'.replace("\\","/")
        self.tcl_commands += f'set_property top_file {{ {src_folder_directory}/TimeController.sv }} [current_fileset]\n'.replace("\\","/")
        with open(file_path, 'w') as tcl_file:
            tcl_file.write(self.tcl_commands)
            
        self.tcl_commands = ''
        
        tcl_path = folder_directory + '\\' + prj_name + '.tcl'
        
        self.run_vivado_tcl(self.vivado_path, tcl_path)
        
    def set_project(self, folder_directory, prj_name):
        tcl_code = "# Set the project name and working directory\n"
        tcl_code += self.generate_set_prj_string(folder_directory,prj_name)
        tcl_code = tcl_code.replace("\\","/")
        tcl_code += '\n'
        
        self.tcl_commands += tcl_code
    
    def create_project(self, part_name):
        tcl_code = "# Create a new project\n"
        tcl_code += self.generate_create_prj_string(part_name)
        tcl_code = tcl_code.replace("\\","/")
        tcl_code += '\n'
        
        self.tcl_commands += tcl_code
    
    def add_src(self, folder_directory,file_type):
        # Get all files in the directory
        all_files = self.get_all_files_in_directory(folder_directory,file_type)
        tcl_code = "# Add the FIFO IP file to the project\n"
        for all_file_path in all_files:
            root, ext = os.path.splitext(all_file_path)
            if ext == '.xdc':
                tcl_code += self.generate_add_constraints_string(all_file_path)
            else:
                tcl_code += self.generate_add_files_string(all_file_path)
            
        #using '\' makes error in vivado.bat. this should be replaced in '/'
        tcl_code = tcl_code.replace("\\","/")
        tcl_code += '\n'
        
        self.tcl_commands += tcl_code
    
    def set_board(self, board_path, board_name):
        tcl_code = "# Set the target board\n"
        tcl_code += self.generate_set_board(board_path, board_name)
        tcl_code = tcl_code.replace("\\","/")
        tcl_code += '\n'
        
        self.tcl_commands += tcl_code
        
    def open_vivado(self, folder_directory,prj_name):
        tcl_code = ''
        tcl_code += 'start_gui\n'
        # tcl_code += f'open_project {folder_directory}/{prj_name}/{prj_name}.xpr\n'
        
        tcl_code = tcl_code.replace("\\","/")
        
        self.tcl_commands += tcl_code
    
    def generate_xsa(self):
        tcl_code = ''
        file_path = os.path.join(self.git_dir, self.target_dir,'make_xsa.tcl')
        if self.make_bit_stream == True:
            bit_addr = os.path.join(self.git_dir,'Vivado_prj_manager','Vitis_main','RFSoC_Main_blk_wrapper.xsa')
            prj_addr = os.path.join(self.git_dir,self.target_dir,'RFSoC_Main_output/RFSoC_Main/RFSoC_Main.xpr')
            tcl_code += f"""
open_project {prj_addr}
write_hw_platform -fixed -include_bit -force -file {bit_addr}
            """
            
            tcl_code = tcl_code.replace("\\","/")
            self.tcl_commands += tcl_code
            with open(file_path, 'w') as tcl_file:
                tcl_file.write(self.tcl_commands)

            self.run_vivado_tcl(self.vivado_path, file_path)
            
    def run(self):
        self.generate_AD9910()
        self.generate_xsa()
        
    
            
if __name__ == "__main__":
    vm = Verilog_maker()
    vm.run()