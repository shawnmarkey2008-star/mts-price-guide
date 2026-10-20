# MTS Price Guide

A local Python/Tkinter desktop calculator developed for Markey Tech Solutions to make IT service estimates more consistent.

## Features

- Searchable catalog of 87 service entries, including a custom combined job.
- Bench/drop-off, remote, and on-site pricing modes.
- Active labor rounded up to 15-minute increments.
- Service and visit minimums, per-unit work, and priority adjustments.
- Parts, markup, supplies, travel, discounts, manually entered tax, and payments.
- Decimal arithmetic for currency calculations.
- Copy or save an estimate summary locally.

## Run

Use Python 3 with Tkinter. No third-party packages are required.

```sh
python mts_price_guide.py
```

On macOS/Linux, use `python3` if needed. If Tkinter is absent, install the Tk support supplied for your Python distribution.

Run the included calculation checks without opening the GUI:

```sh
python mts_price_guide.py --self-test
```

## Calculation model

For ordinary jobs, labor is the greatest of the service minimum times units, the visit minimum, and the rounded time charge. A priority premium is added to labor. Marked-up parts, supplies, travel, discount, and a manually entered tax amount produce the total. Payments reduce the displayed balance.

The diagnostic entry has a separate bench-only, 30-minute cap. Combined work should use one agreed scope so overlapping diagnosis and labor are not charged twice. Unattended transfers are not active labor.

## Customize

Edit `SERVICES` to change the catalog permanently. In-window rate overrides reset when selecting another service or location. The catalog is a historical project snapshot, not a current public price commitment. Confirm scope and an approved quote before billing.

The app does not determine tax rates or legal tax treatment; the tax field is a manually supplied amount. It is an estimating tool, not an accounting or invoicing system.

## Privacy

No customer records or saved quotes are included. The application runs locally and does not need internet access. Quote summaries can contain customer information and are ignored by Git under the default `MTS_Quote_*.txt` filename pattern. Keep any differently named exports private as well.

## Validation

The bundled calculation self-test covers rounding, minimums, parts, payments, priority, units, and invalid inputs. Desktop GUI behavior is not verified in this release environment.
