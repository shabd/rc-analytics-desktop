import numpy as np


class IronAnalysis: 


    def __init__(self):
        self.known_samples = {
            "SARM146": {"Constant": 0.1988},
            "SARM131": {"Constant": 0.2147},
            "NIST64C":{"Constant":0.2499},
            "SARM144":{"Constant":0.3687},
            "AMIS0388": {"Constant": 0.1798}
        }
        self.known_values = [19.88,21.47,24.99,36.87,17.98]

        self.factor_average = None 
        self.tested_samples = []
        self.know_sample_results = []
        self.FeO_constant = 1.2865
        
    def calculate_factors(self, value_dict):
        self.know_sample_results = []

        print("Calculate factors ", value_dict)
        factors = []
        
        # 1. First calculate all  the factors for CRMS
        for sample, values in value_dict.items():
            grams, ml ,_ = values
            factor = grams * self.known_samples[sample]['Constant']/ ml
            self.known_samples[sample]['Factor'] = factor
            factors.append(factor)

            
        # 2. Get the average 
        self.factor_average = sum(factors)/ len(factors)
        # self.standard_deviation = np.std(factors)
        # self.coefficient_of_variation = (self.standard_deviation / self.factor_average) * 100

        
        # 3. We need to cal %Fe and the bias 
        for sample, values in value_dict.items():
            grams, ml, known_value = values 
            percent_fe = (self.factor_average *ml)/grams*100
            bias = (percent_fe - known_value)
            iron_oxide = percent_fe * self.FeO_constant
            self.known_samples[sample].update({
                "%Fe": percent_fe,
                "Known Value" : known_value,
                "Bias": bias,
                "FeO": iron_oxide,
            })
         
            self.know_sample_results.append([
                             sample,grams, ml, round(self.known_samples[sample]['Factor'] , 6), round(percent_fe, 2), known_value, round(bias, 2), round(iron_oxide, 2)
                        ])
            
        return self.know_sample_results
    
    def add_and_calculate_sample(self, ref_id, grams, ml,edit=False,index=None):
        if not self.factor_average:
            raise ValueError("Average factor has not been calculated. Please run calculate_factors first.")

        cal_percent_fe = (self.factor_average * ml) / grams * 100
        calc_Fe0 = cal_percent_fe * self.FeO_constant
        if edit:
            self.tested_samples[index] = [ref_id, float(grams), ml, round(cal_percent_fe, 2), round(calc_Fe0, 2)]
        else:
            self.tested_samples.append([ref_id, float(grams), ml, round(cal_percent_fe, 2), round(calc_Fe0, 2)])

        return self.tested_samples
   


# # # Example usage
# analysis = IronAnalysis()

# # Calculating factors, %Cr, and bias for known samples
# # TODO : if Bias is more than 0.3 then , block step 2 
# analysis.calculate_factors({
#     "SARM146": (0.2001, 7.26, 19.88),
#     "SARM131": (0.2004, 8.08, 21.47),
#     "NIST64C": (0.2000, 9.25, 24.99),
#     "SARM144":(0.2001, 13.30, 36.87),
#     "AMIS0388":(0.2002, 6.77, 17.98),
# })

# # Output the results for the known samples
# for sample, info in analysis.known_samples.items():
#     print(f"{sample}: Factor={info['Factor']}, %Fe={info['%Fe']}, Bias={info['Bias']}, %FeO={info['FeO']}")

# analysis.add_and_calculate_sample("RCI1234", 0.2000, 6.73)
# # analysis.add_and_calculate_sample("RCI1235", 0.2003, 18.07)
# # analysis.add_and_calculate_sample("RCI12589", 0.2004, 18.07)
# # Save the results to a PDF file
# print(analysis.tested_samples)