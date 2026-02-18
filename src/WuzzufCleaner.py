import pandas as pd
from pandas import DataFrame
import html

class WuzzufCleaner:
    def _clean_html_encoding(self, df: DataFrame):
        str_cols = df.select_dtypes(include=['object', 'string']).columns

        df[str_cols] = df[str_cols].apply(
            lambda col: col.map(lambda x: html.unescape(x) if isinstance(x, str) else x)
        )

        return df

    def _clean_company(self, df: DataFrame):
        df['company'] = df['company'].str.removesuffix(' -')
        return df

    def _clean_emp_type(self, df: DataFrame):
        arabic_to_english = {
            "دوام كامل": "Full Time",
            "دوام جزئي": "Part Time",
            "تدريب": "Internship",
            "عمل حر / مشروع": "Freelance / Project",
            "وردية": "Shift Based",
            "حدث": "Event"
        }

        df['employment_type'] = df['employment_type'].replace(arabic_to_english)
        return df

    def _clean_exp_lvl(self, df: DataFrame):
        arabic_to_english_exp = {
            "ذو خبرة": "Experienced",
            "مستوى مبتدئ": "Entry Level",
            "غير محدد": "Not specified",
            "إدارة عليا": "Senior Management",
            "مدير": "Manager"
        }

        df['experience_lvl'] = df['experience_lvl'].replace(arabic_to_english_exp)

        title_to_level_map = {
            'intern': 'Student',
            'trainee': 'Student',

            'junior': 'Entry Level',
            'jr': 'Entry Level',

            'senior': 'Experienced',
            'sr': 'Experienced',

            'lead': 'Manager',
            'principal': 'Manager',
            'manager': 'Manager',

            'head': 'Senior Management',
            'director': 'Senior Management',
        }

        def infer_level_from_title(title: str):
            title = title.lower()

            for keyword, level in title_to_level_map.items():
                if keyword in title:
                    return level

            return None

        mask = df['experience_lvl'] == 'Not specified'

        df.loc[mask, 'experience_lvl_inferred'] = (
            df.loc[mask, 'job_title']
            .apply(infer_level_from_title)
        )

        mask = ((df['experience_lvl'] == 'Not specified') & (~df['experience_lvl_inferred'].isna()))

        df.loc[mask, 'experience_lvl'] = df.loc[mask, 'experience_lvl_inferred']

        df.drop(columns=['experience_lvl_inferred'], inplace=True)

        return df

    def _clean_years(self, df: DataFrame):
        df['years_of_experience'] = df['years_of_experience'].str.removeprefix('·')

        df.loc[~df['years_of_experience'].isna(), 'min_years_of_exp'] = df.loc[
            ~df['years_of_experience'].isna(), 'years_of_experience'].apply(
            lambda x: x[0:2] if x[0].isdigit() and len(x) > 1 and x[1].isdigit()
            else x[0] if x[0].isdigit()
            else None
        )

        return df

    def _fill_years(self, df: DataFrame):
        exp_dict = df.groupby('experience_lvl')['min_years_of_exp'].agg(
            lambda x: x.mode().iloc[0] if not x.mode().empty else None).to_dict()

        df['min_years_of_exp'] = df['min_years_of_exp'].fillna(df['experience_lvl'].map(exp_dict))

        df.loc[df['experience_lvl'] == 'Student', 'min_years_of_exp'] = '0'

        df['min_years_of_exp'] = pd.to_numeric(df['min_years_of_exp'], errors='coerce')

        df['min_years_of_exp'] = df['min_years_of_exp'].fillna(
            df['min_years_of_exp'].median()
        )

        return df

    def _clean_skill(self, df: DataFrame):
        df['skill'] = df['skill'].apply(lambda x: x.removeprefix('·').strip())
        return df

    def _fill_work_loc(self, df: DataFrame):
        title_to_loc = {
            'remote': 'Remote',
            'onsite': 'On-site',
            'on site': 'On-site',
            'office': 'On-site',
            'hybrid': 'Hybrid'
        }

        def infer_loc_from_title(title: str):
            title = title.lower()
            for keyword, loc in title_to_loc.items():
                if keyword in title:
                    return loc
            return None

        mask = df['work_arrangement_type'].isna()
        df.loc[mask, 'work_arrangement_type'] = df.loc[mask, 'job_title'].apply(infer_loc_from_title)

        work_loc_dict = df.groupby(['employment_type', 'experience_lvl', 'min_years_of_exp'])['work_arrangement_type'] \
            .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None).reset_index()

        df = df.merge(work_loc_dict, on=['employment_type', 'experience_lvl', 'min_years_of_exp'], how='left', suffixes=('', '_fill'))
        df['work_arrangement_type'] = df['work_arrangement_type'].fillna(df['work_arrangement_type_fill'])
        df = df.drop(columns=['work_arrangement_type_fill'])


        df['work_arrangement_type'] = df['work_arrangement_type'].fillna(
            df['work_arrangement_type'].mode().iloc[0]
        )

        return df

    def clean(self, data: str, filename: str):
        df: DataFrame = pd.read_csv(f'D:\\Projects\\PycharmProjects\\Jobify\\data\\{data}.csv')
        df = self._clean_html_encoding(df)
        df = self._clean_company(df)
        df = self._clean_emp_type(df)
        df = self._clean_years(df)
        df = self._clean_skill(df)
        df = self._clean_exp_lvl(df)
        df = self._fill_years(df)
        df = self._fill_work_loc(df)
        df.drop(columns=['years_of_experience'], inplace=True)
        df.to_csv(f'D:\\Projects\\PycharmProjects\\Jobify\\data\\{filename}.csv', index=False)
