

class ChromeOreAnalysis: 


    def __init__(self):
        self.known_samples = {
            "SARM146": {"Constant": 0.3209},
            "SARM131": {"Constant": 0.2866},
            "AMIS0388": {"Constant": 0.2746}
        }
        
        self.factor_average = None 
        self.tested_samples = []
        self.know_sample_results = []
        self.CR2O3_constant = 1.4615
        
    def calculate_factors(self, value_dict):
        self.know_sample_results = []

        print(f"value_dict: {value_dict}")
        factors = []
        
        # 1. First calculate all  the factors for CRMS
        for sample, values in value_dict.items():
            grams, ml ,_ = values
            factor = grams * self.known_samples[sample]['Constant']/ ml
            self.known_samples[sample]['Factor'] = factor
            factors.append(factor)

            
        # 2. Get the average 
        self.factor_average = sum(factors)/ len(factors)
        
        # 3. We need to cal %Cr and the bias 
        for sample, values in value_dict.items():
            grams, ml, known_value = values 
            percent_cr = (self.factor_average *ml)/grams*100
            bias = (percent_cr - known_value)
            self.known_samples[sample].update({
                "%Cr": percent_cr,
                "Known Value" : known_value,
                "Bias": bias
            })
         
            self.know_sample_results.append([
                            sample, grams, ml, round(self.known_samples[sample]['Factor'] , 6), round(percent_cr, 2), known_value, round(bias, 2)
                        ])
        print(self.known_samples)
        return self.know_sample_results
            
    def add_and_calculate_sample(self, ref_id, grams, ml):
        if not self.factor_average:
            raise ValueError("Average factor has not been calculated. Please run calculate_factors first.")

        cal_percent_cr = (self.factor_average * ml) / grams * 100
        calc_cr2o3 = cal_percent_cr * self.CR2O3_constant
        self.tested_samples.append([ref_id, float(grams), ml, round(cal_percent_cr, 2), round(calc_cr2o3, 2)])

        return self.tested_samples
   


# # Example usage
# analysis = ChromeOreAnalysis()

# # Calculating factors, %Cr, and bias for known samples
# # TODO : if Bias is more than 0.3 then , block step 2 
# analysis.calculate_factors({
#     "SARM146": (0.2004, 21.12, 32.09),
#     "SARM131": (0.2001, 19.19, 28.66),
#     "AMIS0388": (0.2000, 17.96,27.46)
# })

# # Output the results for the known samples
# for sample, info in analysis.known_samples.items():
#     print(sample)
#     print(info)
#     print(analysis.factor_average)

# # analysis.add_and_calculate_sample("RCI1234", 0.2001, 18.08)
# # analysis.add_and_calculate_sample("RCI1235", 0.2003, 18.07)
# # analysis.add_and_calculate_sample("RCI12589", 0.2004, 18.07)
# # # Save the results to a PDF file
# # analysis.save_results_to_pdf("samples_results.pdf")