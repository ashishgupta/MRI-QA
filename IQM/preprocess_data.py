import pandas as pd 
import numpy as np 


def create_data_file(label_file, out_file):
    data_file = './x_abide.csv'
    # read the label csv file
    label_df = pd.read_csv(label_file, header=None)
    # assign column names
    label_df.columns = ['subject_id', 'label']
    # set the column with subject id as index of dataframe
    label_df = label_df.set_index('subject_id')
    # change the label for negative class from -1 to 0
    label_df = label_df.replace(-1, 0)
    # read the data csv file
    data_df = pd.read_csv(data_file)
    # remove the non-informative features of spacing
    data_df = data_df.drop(columns=['spacing_x', 'spacing_y', 'spacing_z'])
    # set the column with subject id as index of dataframe
    data_df = data_df.set_index('subject_id')
    # slice the training data from the entire data corpus
    data_df_select = data_df[data_df.index.isin(label_df.index)]
    # ensure the bijective mapping between labels and data in case of missing data
    label_df = label_df[label_df.index.isin(data_df_select.index)]
    # sort the dataframe by the subject_id as index
    label_df.sort_index(inplace=True)
    data_df_select.sort_index(inplace=True)
    # concatenate the data with the label
    data_df_cat = pd.concat([data_df_select, label_df], axis=1)
    # debug
    print(data_df_cat.shape)
    # write dataframe to csv without index and header
    data_df_cat.to_csv(out_file, sep=',', header=False, index=False)



def create_train_val_files(label_files, out_files):
    """create training and validation data files for abide 1
    
    Arguments:
        label_files {[type]} -- [description]
        out_files {[type]} -- [description]
    """
    for i in range(len(label_files)):
        label_file = label_files[i]
        out_file = out_files[i]
        create_data_file(label_file, out_file)
        print(f'created {out_file}')


def create_test_file():
    """test data file for DS030 dataset
    """
    data_file = './x_ds030.csv'
    label_file = './y_ds030.csv'
    out_file = './ds030_test.csv'

    # read the data csv file
    data_df = pd.read_csv(data_file)
    # remove the non-informative features of spacing
    data_df = data_df.drop(columns=['spacing_x', 'spacing_y', 'spacing_z'])
    # read the label csv file
    label_df = pd.read_csv(label_file)
    # prune out the labels without 1 or -1
    label_df = label_df[label_df.rater_1 != 0]
    # replace the label -1 with 0
    label_df = label_df.replace(-1, 0)
    # remove the column on site
    label_df = label_df.drop(columns=['site'])
    # set the column with subject id as index of dataframe
    label_df = label_df.set_index('subject_id')
    # set the column with subject id as index of dataframe
    data_df = data_df.set_index('subject_id')
    # rename label column
    label_df = label_df.rename(columns={'rater_1': 'label'})

    # sort the dataframe by the subject_id as index
    label_df.sort_index(inplace=True)
    data_df.sort_index(inplace=True)

    # slice the training data from the entire data corpus
    data_df = data_df[data_df.index.isin(label_df.index)]
    # ensure the bijective mapping between labels and data in case of missing data
    label_df = label_df[label_df.index.isin(data_df.index)]

    # concatenate the data with the label
    data_df_cat = pd.concat([data_df, label_df], axis=1)

    # debug
    # print(data_df_cat.shape)
    # write dataframe to csv without index and header
    data_df_cat.to_csv(out_file, sep=',', header=False, index=False)

    #debug
    # print(data_df_cat.head())

def test_loading():
    data_file = './abide_train.csv'
    raw_data = np.genfromtxt(data_file, delimiter=',')
    data = raw_data[:,:-1]
    label = raw_data[:,-1]
    print(data.shape)
    print(label.shape)


def prune_features(data_file):
    data_df = pd.read_csv(data_file)
    print(data_df.head())
    print(data_df.columns)
    print(data_df.dtypes)

def label_proportion():
    abide_train = './abide_train.csv'
    abide_val = './abide_val.csv'
    ds030_test = './ds030_test.csv'

    at = pd.read_csv(abide_train, header=None)
    av = pd.read_csv(abide_val, header=None)
    ds = pd.read_csv(ds030_test, header=None)

    print(at[65].value_counts())
    print(av[65].value_counts())
    print(ds[65].value_counts())

def try_upsampling():
    abide_train = './abide_train.csv'
    abide_val = './abide_val.csv'
    ds030_test = './ds030_test.csv'

    at = pd.read_csv(abide_train, header=None)
    av = pd.read_csv(abide_val, header=None)
    ds = pd.read_csv(ds030_test, header=None)

    at_class_0 = at[at[65] == 0]
    at_class_1 = at[at[65] == 1]

    av_class_0 = av[av[65] == 0]
    av_class_1 = av[av[65] == 1]

    print(at_class_0.shape)
    print(at_class_1.shape)

    print(av_class_0.shape)
    print(av_class_1.shape)

    av_count_0 = av_class_0[65].value_counts()
    av_count_1 = av_class_1[65].value_counts()

    av_count = av[65].value_counts()
    print(av_count[0])
    print(av_count[1])

    count_0 = av_count[0]
    count_1 = av_count[1]

    if count_0 > count_1:
        av_class_1_over = av_class_1.sample(count_0, replace=True)
        av_over = pd.concat([av_class_0, av_class_1_over], axis=0)
    else:
        av_class_0_over = av_class_0.sample(count_1, replace=True)
        av_over = pd.concat([av_class_1, av_class_0_over], axis=0)
    
    print(av_over[65].value_counts())

def balance_classes(df):
    df_class_0 = df[df[65]==0]
    df_class_1 = df[df[65]==1]
    df_count = df[65].value_counts()
    count_0 = df_count[0]
    count_1 = df_count[1]

    if count_0 > count_1:
        df_class_1_over = df_class_1.sample(count_0, replace=True)
        df_over = pd.concat([df_class_0, df_class_1_over], axis=0)
    elif count_0 < count_1:
        df_class_0_over = df_class_0.sample(count_1, replace=True)
        df_over = pd.concat([df_class_1, df_class_0_over], axis=0)
    else:
        df_over = df
    
    return df_over

    
def test_balance_classes():
    abide_train = './abide_train.csv'
    abide_val = './abide_val.csv'
    ds030_test = './ds030_test.csv'

    at = pd.read_csv(abide_train, header=None)
    av = pd.read_csv(abide_val, header=None)
    ds = pd.read_csv(ds030_test, header=None)

    at_b = balance_classes(at)
    av_b = balance_classes(av)
    ds_b = balance_classes(ds)

    print(at[65].value_counts())
    print(at_b[65].value_counts())

    print(av[65].value_counts())
    print(av_b[65].value_counts())

    print(ds[65].value_counts())
    print(ds_b[65].value_counts())






if __name__=='__main__':
    # label_files = ['./train_2.csv', './val_2.csv']
    # out_files = ['./abide_train.csv', './abide_val.csv']
    # create_train_val_files(label_files, out_files)
    # create_test_file()
    # test_loading()
    # prune_features('./x_abide.csv')
    # label_proportion()
    # try_upsampling()
    test_balance_classes()




