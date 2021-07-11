import math

class SeqSearch:
    
    def __init__(self, data, tally_factor=0, sa_factor=0):
        
        self.tally_factor = tally_factor
        self.sa_factor = sa_factor
        
        fl_matrix = SeqSearch.create_rotations(data)
        fl_matrix.sort()
        
        self.sa = self.sa_index(fl_matrix)
        
        f_string = SeqSearch.get_column(fl_matrix, 0)
        l_string = SeqSearch.get_column(fl_matrix, -1)
        
        self.fl_matrix = {'first':SeqSearch.compress_first(f_string), 'last':l_string}
        self.tally = self.tally_matrix()

    
    def create_rotations(data):
        matrix = []
        double_data = data + data
        # Create all rotations of the input string
        for i in range(0,len(data)):
            matrix.append(double_data[i:i+len(data)])
        return matrix
    
    def get_column(matrix, column):
        column_string = ''
        for i in range(0,len(matrix[0])):
            column_string += matrix[i][column] 
        return column_string

    def tally_matrix(self):
   
        chars = (set(self.fl_matrix['last'])-set('$'))
        tally = {}
        cnts = {}
        for c in chars:
            tally[c]=[]
            cnts[c]=0
        
        iteration = 0;
        for c in self.fl_matrix['last']:
            if c!='$':
                cnts[c] = cnts[c] + 1
            if (self.tally_factor==0) or (iteration%self.tally_factor==0) :
                for ch in chars:
                    tally[ch].append(cnts[ch])
            iteration+=1
        return tally
    
    def sa_index(self,rotations): #rotations
        sa = {}
        iteration = 0
        strlen = len(rotations[0])
        for row in rotations:
            if (self.sa_factor==0) or (((row.index('$')-((strlen-1)%self.sa_factor))%self.sa_factor)==0):
                sa[iteration] = len(row) - row.index('$') - 1
            iteration+=1
        return sa
    
    def compress_first(first_str):
        first = []
        ch=first_str[0]
        for i in range(0,len(first_str)):
            if first_str[i]==ch:
                continue
            first.append((ch,i))
            ch = first_str[i]
        first.append((ch,len(first_str)))
        return first

    
    def find_row_by_last(self,ch,rank):
        for i in range(0,len(self.fl_matrix['first'])):
            if self.fl_matrix['first'][i][0]==ch:
                if i==0: 
                    return rank
                else:
                    return self.fl_matrix['first'][i-1][1]+rank
                
    
    def get_rank_by_tally(self, ch, row_number):

        if row_number >= len(self.fl_matrix['last']):
            return -1

        if self.tally_factor==0:
            return self.tally[ch][row_number]-1
        elif row_number%self.tally_factor==0:
            return self.tally[ch][int(row_number/self.tally_factor)]-1
        else:
            cnt=0
            if (row_number/self.tally_factor >= self.tally_factor/2 and (math.ceil(row_number/self.tally_factor)<len(self.tally[ch]))):
                row=row_number+1;
                while(row%self.tally_factor!=0):
                    if self.fl_matrix['last'][row] == ch:
                        cnt+=1
                    row+=1;
                if self.fl_matrix['last'][row]==ch:
                    cnt+= 1

                return self.tally[ch][int(row/self.tally_factor)] - cnt - 1 


            else:
                row=row_number;
                while(row%self.tally_factor!=0):
                    if self.fl_matrix['last'][row] == ch:
                        cnt+=1
                    row-=1;           

                return self.tally[ch][math.floor(row/self.tally_factor)] + cnt - 1
       
    
    def get_offset_by_sa(self,rows_list):
        offsets = []
        
        for row in rows_list:
            cnt=0;
            i = row
            while (not (i in self.sa)):
                cnt+=1
                ch = self.fl_matrix['last'][i]
                i = self.find_row_by_last(ch , self.get_rank_by_tally(ch,i))
            offsets.append(self.sa[i]+cnt)   
        return offsets
    
    
    
    def query(self, pattern):
        pos = len(pattern)-1
        ch = pattern[pos]
        rows = []
        
        for i in range(0,len(self.fl_matrix['first'])):
            if self.fl_matrix['first'][i][0] == ch:
                if i == 0:
                    rows = [i for i in range(0,self.fl_matrix['first'][i][1])]
                else:
                    rows = [i for i in range(self.fl_matrix['first'][i-1][1],self.fl_matrix['first'][i][1])]
        
        
        while(pos>0):
            tmp_rows = []
            for row in rows:
                if self.fl_matrix['last'][row] == pattern[pos-1]:
                    c = pattern[pos-1]
                    x = self.find_row_by_last(c,self.get_rank_by_tally(c,row))
                    tmp_rows.append(x)
            if not tmp_rows:
                return []
            pos-=1
            rows = tmp_rows
        
        return self.get_offset_by_sa(rows)
    
    
    
