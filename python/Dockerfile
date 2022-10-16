FROM python
ENV PATH /usr/src/app/bin:$PATH
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests
RUN pip install pandas

COPY bin/* ./
COPY python-manager.sh /
ENTRYPOINT [ "/python-manager.sh" ]