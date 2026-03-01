# labs

- name: Deploy app
  kubernetes.core.k8s:
    template: dep-app.yaml.j2
  tags: [app, deploy]

- name: Deploy ingress
  kubernetes.core.k8s:
    template: ingress.yaml.j2
  tags: [ingress, deploy]

- name: Deploy database
  kubernetes.core.k8s:
    template: postgres.yaml.j2
  tags: [db, deploy]
