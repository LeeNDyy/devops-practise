for i in {1..10}; do 
  echo "=== Запрос $i ==="; 
  curl -s http://158.160.139.54/ | head -5; 
  sleep 0.5; 
done
