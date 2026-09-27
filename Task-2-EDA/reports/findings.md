# Task 2 - Exploratory Data Analysis Findings Report

## Superstore Sales Dataset - Key Analytical Findings

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| Total Orders | 9,993 |
| Total Columns | 23 |
| Date Range | 2016-01-02 to 2019-12-30 |
| Categories | 3 |
| Regions | 4 |
| Customer Segments | 3 |

---

## 2. Descriptive Statistics

### Numeric Variables Summary

| Statistic | Sales | Quantity | Discount | Profit |
|-----------|-------|----------|----------|--------|
| Mean | $229.85 | 3.79 | 0.16 | $28.66 |
| Median | $54.48 | 3.00 | 0.20 | $8.67 |
| Std Dev | $623.28 | 2.23 | 0.21 | $234.27 |
| Min | $0.44 | 1 | 0.00 | $-6,599.98 |
| Max | $22,638.48 | 14 | 0.80 | $8,399.98 |

### Key Observations
- Sales distribution is **right-skewed** (mean > median), indicating most orders are small with a few large ones.
- Profit has negative values for 18.7% of orders - these are loss-making transactions.
- Discount ranges from 0% to 80%, with an average of 15.6%.

---

## 3. Distribution Analysis

### Category Distribution
Category
Office Supplies    6026
Furniture          2120
Technology         1847

### Segment Distribution
Segment
Consumer       5191
Corporate      3020
Home Office    1782

### Profit Distribution
- Positive profit orders: 8,058 (80.6%)
- Negative profit (loss) orders: 1,870 (18.7%)
- Break-even orders: 65 (0.7%)

---

## 4. Trend Analysis

### Yearly Sales & Profit
               Sales    Profit
OrderYear                     
2016       483966.13  49556.03
2017       470532.51  61618.60
2018       609205.60  81795.17
2019       733215.26  93439.27

### Monthly Sales Trend
- Peak sales month: Nov ($271,693.75)
- Lowest sales month: Feb ($132,721.36)
- Seasonal pattern shows higher sales in Q4 (holiday season)

### Top Performing Categories by Year
Category   Furniture  Office Supplies  Technology
OrderYear                                        
2016       156911.48        151776.41   175278.23
2017       170518.24        137233.46   162780.81
2018       198901.44        183939.98   226364.18
2019       215387.27        246097.18   271730.81

---

## 5. Relationship Analysis

### Correlation Matrix
           Sales  Quantity  Discount  Profit
Sales     1.0000    0.2008   -0.0282  0.4791
Quantity  0.2008    1.0000    0.0087  0.0662
Discount -0.0282    0.0087    1.0000 -0.2195
Profit    0.4791    0.0662   -0.2195  1.0000

### Key Correlations
- Sales vs Profit: 0.4791 - moderate positive correlation
- Sales vs Discount: -0.0282 - weak positive correlation
- Profit vs Discount: -0.2195 - negative correlation (discounts erode profit)
- Profit vs Quantity: 0.0662 - weak positive correlation

### Category Profitability
                     Sales     Profit
Category                             
Furniture        741718.42   18463.33
Office Supplies  719047.03  122490.80
Technology       836154.03  145454.95

### Segment Profitability
                  Sales     Profit
Segment                           
Consumer     1161401.34  134119.21
Corporate     706146.37   91979.13
Home Office   429371.78   60310.74

---

## 6. Outlier Detection

### IQR-Based Outlier Analysis

- **Sales**:
  - Q1=17.28, Q3=209.94, IQR=192.66
  - Bounds: [-271.71, 498.93]
  - Low outliers: 0 (0.00%)
  - High outliers: 1167 (11.68%)

- **Quantity**:
  - Q1=2.00, Q3=5.00, IQR=3.00
  - Bounds: [-2.50, 9.50]
  - Low outliers: 0 (0.00%)
  - High outliers: 170 (1.70%)

- **Discount**:
  - Q1=0.00, Q3=0.20, IQR=0.20
  - Bounds: [-0.30, 0.50]
  - Low outliers: 0 (0.00%)
  - High outliers: 856 (8.57%)

- **Profit**:
  - Q1=1.73, Q3=29.36, IQR=27.63
  - Bounds: [-39.72, 70.81]
  - Low outliers: 604 (6.04%)
  - High outliers: 1277 (12.78%)


### Key Findings on Outliers
- Sales outliers: 1167 orders with unusually high values
- Profit outliers: 604 extreme losses and 1277 extreme gains
- These outliers represent bulk purchases and high-value corporate orders

---

## 7. Unusual Patterns

### High-Discount, Loss-Making Orders
- 922 orders (9.2% of total) with discount >=50% resulted in losses
- **Primary affected categories**: Furniture, Office Supplies, Technology

### Top Loss-Making Products
      - Cubify CubeX 3D Printer Double Head Print: $-9,239.97
      - GBC DocuBind P400 Electric Binding System: $-6,859.39
      - Lexmark MX611dhe Monochrome Laser Printer: $-5,269.97
      - GBC Ibimaster 500 Manual ProClick Binding System: $-5,098.57
      - GBC DocuBind TL300 Electric Binding System: $-4,162.03
      - Cubify CubeX 3D Printer Triple Head Print: $-3,839.99
      - Fellowes PB500 Electric Punch Plastic Comb Binding Machine w: $-3,431.67
      - Chromcraft Bull-Nose Wood Oval Conference Tables & Bases: $-3,107.53
      - Ibico EPK-21 Electric Binding System: $-2,929.48
      - Bush Advantage Collection Racetrack Conference Table: $-2,545.26

### Top Revenue-Generating Products
      - Canon imageCLASS 2200 Advanced Copier: $61,599.82
      - Fellowes PB500 Electric Punch Plastic Comb Binding Machine w: $27,453.38
      - Cisco TelePresence System EX90 Videoconferencing Unit: $22,638.48
      - HON 5400 Series Task Chairs for Big and Tall: $21,870.58
      - GBC DocuBind TL300 Electric Binding System: $19,823.48
      - GBC Ibimaster 500 Manual ProClick Binding System: $19,024.50
      - Hewlett Packard LaserJet 3310 Copier: $18,839.69
      - HP Designjet T520 Inkjet Large Format Printer - 24" Color: $18,374.90
      - GBC DocuBind P400 Electric Binding System: $17,965.07
      - High Speed Automatic Electric Letter Opener: $17,030.31

---

## 8. Business Questions Answered

### Q1: What category generates the most revenue?
**Answer:** Technology ($836,154.03, 36.4% of total)

### Q2: Which customer segment is most profitable?
**Answer:** Consumer ($134,119.21)

### Q3: Which region has the highest sales?
**Answer:** West ($725,457.82, 31.6% of total)

### Q4: What is the company's overall profitability?
**Answer:** Revenue=$2,296,919.49, Profit=$286,409.08, Margin=12.47%

### Q5: How does discount affect profitability?
**Answer:** Low-discount (<20%) avg profit/order: $67.04; High-discount (>=50%) avg profit/order: $-105.28 - discounts reduce profitability

### Q6: Which shipping mode dominates sales?
**Answer:** Standard Class ($1,357,934.37)

### Q7: Are there seasonal trends in sales?
**Answer:** Peak in Nov ($271,693.75); Lowest in Feb ($132,721.36)

---

## 9. Key Conclusions

1. **Revenue Concentration**: The top category accounts for 36.4% of all revenue.
2. **Profitability Challenge**: 18.7% of orders are loss-making, primarily due to excessive discounting.
3. **Seasonal Opportunity**: Q4 shows peak sales - inventory and staffing should scale accordingly.
4. **Segment Disparity**: Consumer segment is most profitable.
5. **Discount Impact**: Orders with discount >=50% frequently result in losses.
6. **Regional Variation**: West leads - regional strategies should be tailored.
7. **Outlier Insight**: Sales outliers represent legitimate bulk orders.

---

## 10. Recommendations

- **Discount Policy**: Implement tiered discount limits based on category.
- **Inventory Planning**: Increase inventory for Q4 peak season in Nov.
- **Product Strategy**: Discontinue or re-price consistently loss-making products.
- **Customer Focus**: Develop retention programs for Consumer segment customers.
- **Regional Optimization**: Expand successful strategies from West to other regions.

---

*Report generated by Task 2 - Exploratory Data Analysis*
*Dataset: Superstore Sales Dataset*
*Generated: 2026-09-27 23:15:29*
