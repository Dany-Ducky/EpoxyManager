# EpoxyManager

> *Sharpen your axe before you chop wood*  
> Tuned for epoxy; may extend to other thermoset / UV-curable / PU formulation systems.

[繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

A desktop workstation for **epoxy adhesive & sealant formulation design**, with ML-driven viscosity prediction, material database management, and full four-language support.

---

## ✨ Features

### 🧪 Formulation Design
- **1K single-component** formulation with three balancing modes: `target_100g`, `phr_100`, `free`
- **2K two-component** formulation with stoichiometry-driven A/B side calculation, EEW / AHEW equivalent balancing, and customizable mixing ratios
- Real-time cost estimation, chlorine content tracking, batch scaling
- Copy-to-Excel with vertical/horizontal layouts

### 📊 ML-Driven Viscosity Prediction
- **5-layer ensemble model**: Gaussian Process Regression + Bayesian Ridge + adaptive k-NN
- Physics-based fallback: Grunberg-Nissan mixing rule, Arrhenius temperature dependence, Krieger-Dougherty for filler systems
- Jaccard-weighted historical correction from your own recipe database
- Auto-activates after ≥2 recipes with viscosity data are saved

### 🧮 Chemistry Toolbox
- **Gel time estimation** by Arrhenius extrapolation across 7 hardener types (DICY / Amine / Anhydride / Imidazole / Mercaptan / Latent / Phenolic)
- **DiBenedetto Tg prediction** from monomer Tg₀/Tg∞ and degree of cure
- **CTE prediction** by rule-of-mixtures with filler volume fraction
- **UV / thermal dual-cure** design with photoinitiator + thermal initiator balancing
- **DSC analysis**: Ti / Tp / ΔH / Ea extraction, catalyst homopolymerization coefficient
- **Thermal balance**: adiabatic temperature rise, heat dissipation estimates

### 🌏 Full Multilingual Support
- Hot-swappable language selector: **繁體中文 / 简体中文 / English / 日本語**
- 596-key translation dictionary covering every UI element, property name, test method, and tooltip
- Legacy CSV compatibility preserved across all languages

### 🎨 Apple-Style UI
- 9 theme colors (blue, violet, pink, red, orange, green, cyan, graphite, black)
- Custom rounded dropdowns, tooltips, segmented buttons
- Consistent typography with system font detection (SF Pro / Segoe UI / Hiragino)

### 📦 Material & Recipe Database
- 8 property categories with 80+ pre-defined fields (Uncured / Curing / Mechanical / Thermal / Chemical / Electrical / Reliability / Custom)
- Customizable material categories (resins, hardeners, accelerators, fillers, additives, etc.) with user-defined slot counts and fields
- Hardener subtype normalization (amine / polyamide / anhydride / mercaptan / imidazole / DICY / phenolic / latent)
- CSV storage for portability

### 🔬 Analytical Tools
- Per-recipe property entry with structured categories (Tg by DSC/DMA/TMA, CTE α1/α2, dielectric Dk/Df, thermal conductivity, lap shear, reflow resistance, PCT/HAST reliability, etc.)
- Viscosity-temperature extrapolation, mix-viscosity for multi-component systems

---

## 🚀 Quick Start

### Requirements
- Python **3.10+**
- Tested on Windows 10/11, macOS, Linux

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
python EpoxyManager.py
```

On first run, the app creates empty databases and config files in the working directory.

---

## 📂 Data Files (Auto-generated, Gitignored)

The app creates these files in your working directory — they contain **your** data and are excluded from version control by default:

| File | Purpose |
|------|---------|
| `epoxy_db.csv` | Material database |
| `recipe_database.csv` | Recipe database with properties |
| `custom_properties.csv` | User-defined property fields |
| `user_prop_definitions.csv` | User-defined property categories |
| `lang_config.json` | Language preference |
| `epoxy_prefs.json` | UI preferences (theme color, DB paths) |
| `custom_categories.json` | Custom hardener subtypes |
| `custom_mat_cats.json` | Custom material categories |
| `mat_col_config.json` | Column visibility configuration |

---

## 🛠 Architecture

- **Single-file Python application** (~5,670 lines) — no external config, no build step
- **UI**: CustomTkinter with custom Apple-style widgets
- **i18n**: 596-key single-source-of-truth dictionary with zh_TW as canonical keys for CSV backward compatibility
- **Data**: CSV-based storage with automatic schema migration
- **ML**: scikit-learn GPR + BayesianRidge + k-NN ensemble with physics-based fallback

---

## 📝 License

MIT License — see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), [scikit-learn](https://scikit-learn.org/), and [NumPy](https://numpy.org/).

Inspired by:
- Confucius, *Analects · Wei Ling Gong* — "工欲善其事，必先利其器"
- Kūkai (Kōbō-Daishi), *Shōryō-shū* — "良工まずその刀を利くし、能書は必ず好筆を用う"
- Abraham Lincoln — *"Give me six hours to chop down a tree and I will spend the first four sharpening the axe."*

---

## 🤝 Contributing

Issues and pull requests welcome. For substantial changes, please open an issue first to discuss what you'd like to change.

If you use EpoxyManager in your work, a ⭐ on the repo is appreciated.
