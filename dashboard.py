import streamlit as st
import pandas as pd
import numpy as np
import base64
import pickle


def main():
    st.title("Ad Ranking")

    st.write('''
        ## Introduction
        Enter Campaign ID and then download the ranked ads as csv
        ''')

    data = pd.read_csv('impression_log.csv')
    cid = st.text_input('Enter Campaign ID')
    
    def score_sites(df, campaign_id):
        new_df = df[df['CampaignId'] == campaign_id]
        eng = df[['Site', 'click', 'engagement']].groupby('Site').agg(['sum','count']).reset_index()
        scores = pd.DataFrame({
            'Site': eng['Site'], 
            'engagement_rate': eng['engagement']['sum']/eng['engagement']['count'],
            'click_through_rate': eng['click']['sum']/eng['engagement']['sum']
            })
        return scores.sort_values('engagement_rate', ascending = False)
    #campaign_id = 't29si1w'
    if st.button('score'):
        st.subheader(f'Given Campaign ID : "{cid}"')
        scored = score_sites(data, cid)
        st.table(scored.head(5))

        st.subheader('Download the scored list of ads as a csv file by clicking the link below.')

        csv  = scored.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="ScoredAds_{cid}.csv">Download csv file</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()