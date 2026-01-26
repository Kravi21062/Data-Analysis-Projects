# 🍔 Food Delivery Time & Rating Analysis Dashboard (Power BI)

An interactive **Power BI dashboard** built on a **10,000+ orders dataset** to analyze delivery performance, late delivery patterns, customer ratings, and cancellations for a Zomato/Swiggy-style food delivery business.

---

## 🚀 Project Overview
This project focuses on tracking and improving food delivery operations by measuring:
- **Average delivery time**
- **On-time vs Late delivery %**
- **Late deliveries by city**
- **Distance vs delivery time relationship**
- **Late % by hour of day (Heatmap)**
- **Customer rating & cancellation rate**

The dashboard includes a modern dark UI theme and interactive filters for deep analysis.

---

## 📊 Dashboard Features
✅ **KPI Cards**
- Total Orders  
- Avg Delivery Time (min)  
- On-Time %  
- Late %  
- Avg Rating  
- Cancellation Rate %  

✅ **Visuals**
- **Delivery Time Trend (Jan–Dec)**
- **Late Deliveries by City (Top cities)**
- **Distance vs Delivery Time Scatter (Orange → Red performance range)**
- **Late % by Hour of Day Heatmap (Traffic-wise insights)**

✅ **Slicers / Filters**
- City  
- Zone  
- Cuisine  
- Weather  
- Traffic Level  

---

## 🛠️ Tools & Technologies
- **Power BI**
- **DAX**
- **Excel / CSV Dataset**
- **Data Modeling**
- **Visualization & Dashboard Design**

---

## 📂 Dataset
Dataset includes **10,000+ records** with fields like:
- `Order_ID`
- `City`, `Zone`, `Cuisine`
- `Order_Date`, `Order_Time`, `Order Hour`
- `Distance_km`
- `Delivery_Time_min`
- `Expected_Time_min`
- `Delay_min`
- `Traffic_Level`, `Weather`
- `Customer_Rating`
- `Cancellation`

---

## 📌 Key DAX Measures (Sample)
```DAX
Total Orders = COUNT(Orders[Order_ID])

Late Orders =
CALCULATE(
    COUNT(Orders[Order_ID]),
    Orders[Delivery_Status] = "Late"
)

Late % = DIVIDE([Late Orders], [Total Orders], 0)

On-Time % = 1 - [Late %]

Avg Delivery Time = AVERAGE(Orders[Delivery_Time_min])
