FROM atlas/analysisbase:21.2.120
ADD . /SS3L_HF
USER atlas
RUN source ~/release_setup.sh && \
    pip install --user odict && \
    sudo chown -R atlas /SS3L_HF && \
    cd /SS3L_HF/HistFitter/ && \
    source ./setup.sh && cd src && make 



