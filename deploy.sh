
apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubectl

docker build -t lautaronavarro/contadordevoleyapp-web-client:latest -t lautaronavarro/contadordevoleyapp-web-client:$SHA -f ./web-client/Dockerfile ./web-client
docker build -t lautaronavarro/contadordevoleyapp-api:latest -t lautaronavarro/contadordevoleyapp-api:$SHA -f ./api/Dockerfile ./api

docker push lautaronavarro/contadordevoleyapp-web-client:latest
docker push lautaronavarro/contadordevoleyapp-api:latest

docker push lautaronavarro/contadordevoleyapp-web-client:$SHA
docker push lautaronavarro/contadordevoleyapp-api:$SHA

export ORIGIN_PATH=$(pwd)

cd ~/.kube && kubectl --kubeconfig=${KUBE_CONFIG_FILE} get nodes

cd ${ORIGIN_PATH}

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.26.1/deploy/static/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.26.1/deploy/static/provider/cloud-generic.yaml


kubectl apply -f k8s
kubectl set image deployments/server-deployment server=stephengrider/multi-server:$SHA
kubectl set image deployments/client-deployment client=stephengrider/multi-client:$SHA