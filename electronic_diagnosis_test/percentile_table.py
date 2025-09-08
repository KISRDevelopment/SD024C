'''This table is obtained from the CCET booklet from the results booklet, Appendices'''

import pandas as pd

#"Percentile_Letter": ["Low","Low","Weak","Weak","Below Average","Below Average","Average","Good","Good","Superior","Superior"],

grade_2 = pd.DataFrame({
        "Percentile_Letter": ["متدني","متدني","ضعيف","ضعيف","أقل من المتوسط","أقل من المتوسط","متوسط","جيد","جيد","متفوق","متفوق"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],

        "test1_Raw_score":[1,2,4,7,9,12,14,17,20,23,25],
        "test1_Modified_standard":[73,75,79,85,89,95,99,105,111,116,120],

        "test2_Raw_score":[1,5,7,14,19,34,55,67,76,84,90],
        "test2_Modified_standard":[77,79,80,83,86,93,103,108,112,116,119],

        "test3_Raw_score":[0,0,1,2,3,4,5,7,8,10,13],
        "test3_Modified_standard":[81,81,84,87,90,93,97,103,106,112,122],

        "test4_Raw_score":[0,0,1,2,3,5,6,8,10,14,17],
        "test4_Modified_standard":[82,82,84,86,89,94,96,100,105,115,121],

        "test5_Raw_score":[2,4,5,7,8,9,11,12,13,14,16],
        "test5_Modified_standard":[67,75,79,87,91,94,102,106,110,114,121],

        "test6_Raw_score":[0,0,1,2,2,3,3,4,5,7,10],
        "test6_Modified_standard":[82,82,86,90,90,94,94,97,101,109,120],
    })

grade_3 = pd.DataFrame({
        "Percentile_Letter": ["متدني","متدني","ضعيف","ضعيف","أقل من المتوسط","أقل من المتوسط","متوسط","جيد","جيد","متفوق","متفوق"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],

        "test1_Raw_score":[2,4,6,9,12,14,17,19,22,24,26],
        "test1_Modified_standard":[71,75,79,85,91,95,101,105,109,111,119],

        "test2_Raw_score":[2,6,16,36,53,63,70,78,82,87,93],
        "test2_Modified_standard":[67,69,74,85,94,100,104,108,110,113,116],

        "test3_Raw_score":[1,2,3,5,8,9,11,13,15,17,21],
        "test3_Modified_standard":[76,78,81,85,92,94,99,103,108,112,121],

        "test4_Raw_score":[0,1,2,5,8,11,14,16,19,22,25],
        "test4_Modified_standard":[75,77,79,84,90,95,101,104,110,115,121],

        "test5_Raw_score":[4,6,7,9,11,12,13,15,16,17,20],
        "test5_Modified_standard":[70,77,80,86,93,96,99,105,109,112,121],

        "test6_Raw_score":[0,1,2,3,4,5,7,9,11,14,18],
        "test6_Modified_standard":[79,82,84,87,89,91,96,101,106,113,123],
    })
 
grade_4 = pd.DataFrame({
        "Percentile_Letter": ["متدني","متدني","ضعيف","ضعيف","أقل من المتوسط","أقل من المتوسط","متوسط","جيد","جيد","متفوق","متفوق"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],

        "test1_Raw_score":[2,6,9,12,14,16,18,21,22,24,26],
        "test1_Modified_standard":[64,73,80,87,91,96,100,107,109,114,118],

        "test2_Raw_score":[8,22,33,55,65,73,77,83,87,90,94],
        "test2_Modified_standard":[58,67,74,89,96,101,104,108,110,112,115],

        "test3_Raw_score":[1,5,7,10,13,15,17,19,21,23,27],
        "test3_Modified_standard":[69,76,80,86,92,96,100,103,107,111,119],

        "test4_Raw_score":[1,4,6,10,14,17,19,22,23,26,28],
        "test4_Modified_standard":[68,73,77,85,92,98,102,108,109,115,119],

        "test5_Raw_score":[5,7,9,11,13,14,15,17,19,21,23],
        "test5_Modified_standard":[70,75,81,87,92,95,98,104,109,115,121],

        "test6_Raw_score":[1,2,3,5,7,9,11,13,17,21,25],
        "test6_Modified_standard":[78,80,82,86,89,93,97,101,108,116,123],
    })

grade_5 = pd.DataFrame({
        
        "Percentile_Letter": ["متدني","متدني","ضعيف","ضعيف","أقل من المتوسط","أقل من المتوسط","متوسط","جيد","جيد","متفوق","متفوق"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],

        "test1_Raw_score":[2,7,9,13,16,19,21,23,24,26,27],
        "test1_Modified_standard":[61,72,77,85,92,99,103,108,110,114,116],

        "test2_Raw_score":[9,39,50,65,73,79,83,87,90,92,96],
        "test2_Modified_standard":[44,68,77,89,96,101,104,107,110,112,115],

        "test3_Raw_score":[6,9,11,16,18,20,22,24,27,30,34],
        "test3_Modified_standard":[70,76,79,88,92,95,99,102,108,113,120],

        "test4_Raw_score":[2,5,8,15,19,21,24,25,26,28,29],
        "test4_Modified_standard":[62,68,74,88,96,100,106,108,109,113,115],

        "test5_Raw_score":[6,9,11,13,15,17,18,20,21,23,25],
        "test5_Modified_standard":[66,74,80,85,91,97,99,105,108,114,119],

        "test6_Raw_score":[1,3,5,7,10,13,16,20,22,25,27],
        "test6_Modified_standard":[73,76,80,83,90,94,100,107,111,116,120],
    })

GRADE_TABLES = {
    "2": grade_2,
    "3": grade_3,
    "4": grade_4,
    "5": grade_5,
}