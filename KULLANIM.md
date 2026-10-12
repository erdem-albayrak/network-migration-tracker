# Network Migration Tracker — toplantı paneli

Bu paket kurgusal portföy verileri içerir. app.py proje köküne, data klasöründeki beş CSV mevcut data klasörüne konur. Eski sürümü yedekleyin. Mevcut pandas ve Streamlit ortamı yeterlidir; ek grafik paketi gerekmez.

Başlatma: `python -m streamlit run app.py`

## Güncelleme
- tasks.csv: Her satır bir iş. Status: Planned, In Progress, Waiting, Completed. Task ID benzersizdir. Phase: Planning, Readiness, Execution, Validation, Acceptance. Start Date, End Date ve Actual Finish YYYY-MM-DD biçimindedir. Actual Finish tamamlanan işin gerçek bitişi için tutulur; Gantt plan tarihlerini gösterir. Yeni görev için yeni bir satır ekleyin. Depends On aynı lokasyondaki önceki görevin Task ID değeridir; Waiting Reason bekleme açıklamasıdır.
- migrations.csv: Lokasyon durumu, Progress Notes, Next Actions ve Last Updated burada güncellenir. İş sayısı ve yüzde tasks.csv üzerinden hesaplanır. Completed durumu müşteri kabulü dahil kapanış tamamlanınca girilir. Görevler değiştiğinde eski notları da gözden geçirin.
- raid.csv: Risk, Assumption, Issue, Dependency kayıtlarının durum ve aksiyonlarını güncelleyin.
- milestones.csv: Kabul gibi önemli teslimleri görev ID ile bağlayın. Durum görevden hesaplanır; hedef tarih ayrıca tutulur.
- changes.csv: Değişiklik talebi, etkisi, karar ve sorumlusunu kaydedin. Onaylı değişikliklerin plan tarihlerini ilgili CSV'lerde güncelleyin.

CSV'leri VS Code/Not Defteri ile düzenleyip UTF-8 olarak kaydedin. Virgül içeren açıklamaları çift tırnak içine alın. Sayfayı yenileyin. Panel kayıt düzenlemez; CSV indirmek kaynak dosyaya yazmaz.

## Toplantı akışı
1. Lokasyon ve iş bazında tamamlanmayı gösterin.
2. Grafiklerde lokasyon ilerlemesini karşılaştırın.
3. Gantt ve Review date üzerinden bugünkü, geciken ve bekleyen işleri inceleyin. Listeler çakışabilir.
4. RAID ve kilometre taşlarında sorumlularla aksiyonları doğrulayın.
5. Değişiklik talepleri hakkında karar verin; toplantı sonrası kaynak CSV'leri güncelleyin.

Örnek başlangıç: 10 lokasyon, 200 iş, 54 tamamlanan iş (%27); 1 kabul edilmiş lokasyon (%10). İşler eşit ağırlıklıdır. Bütçe, efor, kritik yol ve otomatik kaynak dengeleme hesaplanmaz. Tüm projeyi etkileyen lokasyon filtreleri yalnızca Migration Status tablosunu; Gantt site filtresi görev listelerini etkiler. Review date üstteki bugüne göre gecikme KPI'sını değiştirmez.

GitHub kendiliğinden güncellenmez. Yerelde doğruladıktan sonra app.py ve data klasörünü commit/push edin.

## Programme Toolkit — Excel'den alınan ek kontroller
Bu bölüm 24 şubelik ayrı referans senaryosudur; 10 lokasyonun rakamlarına eklenmez. Excel verileri CSV'ye aktarılmıştır, Excel ile canlı bağlantı yoktur. Başlangıç rapor tarihi 2026-10-02.
- programme_plan.csv: baseline, forecast, actual, Complete (0–1), Effort days. Kayma ve efor ağırlıklı ilerleme hesaplanır.
- budget.csv: approved, planned, actual, remaining forecast (USD). Forecast ve variance hesaplanır.
- resources.csv: Ekim 2026 kapasite ve atanan günler. Kullanım ve kapasite açığı hesaplanır.
- raci.csv: R/A/C/I; faaliyet başına tek A.
- programme_raid.csv: risk için probability/impact 1–5; score otomatik.
- actions.csv ve decisions.csv: durum, tarih, sorumlu, referans. Gecikme reporting date'e göre hesaplanır.
- programme_milestones.csv: baseline/forecast/actual; kayma ve durum hesaplanır.
Budget örneği: approved $1,000,000, actual $700,000, forecast $1,100,000; overspend $100,000 (%10). Resources örneği: Migration Engineer 66 gün kapasite / 72 gün atama; açık 6 gün. Efor ağırlıklı ilerleme %64.1. RAG Amber.
Kaynak: kullanıcı tarafından gönderilen Network_Transformation_PM_Toolkit(1).xlsx (Dashboard, Project Plan, Milestones, RAID, Budget, Resources, RACI, Actions ve Guide sayfaları). Orijinal Excel değiştirilmedi.
