"""Dashboard-only translations. Never change NASA data or verifier outputs.

English is the default. Russian helps human developers inspect the UI.
Source strings, identifiers and machine-readable evidence stay unchanged.
"""
from __future__ import annotations

from collections.abc import MutableMapping
import re

LANGUAGES = ("en", "ru")
LANGUAGE_KEY = "ui_language"

# Keep translation keys stable as labels evolve.
_TRANSLATIONS = {
    "mc_subtitle": ("Microgravity Combustion Evidence Platform", "Платформа научных данных о горении в микрогравитации"),
    "mc_nav_overview": ("Overview", "Обзор"),
    "mc_nav_explore": ("Explore", "Исследование"),
    "mc_nav_search": ("Search", "Поиск"),
    "mc_nav_verify": ("Verify", "Проверка"),
    "mc_nav_ledger": ("Evidence Ledger", "Журнал доказательств"),
    "mc_nav_methods": ("Methods & Limitations", "Методы и ограничения"),
    "mc_overview_heading": ("Mission overview", "Обзор миссии"),
    "mc_overview_intro": ("Two NASA investigations, two distinct scientific domains; source-linked records only.", "Два исследования NASA, две разные физические области; только записи со ссылками на первоисточники."),
    "mc_d4_not_evp": ("D4 QC categories describe audited records, not NASA-EVP claim verdicts.", "Категории D4 QC относятся к проверке данных, а не к вердиктам NASA-EVP по утверждениям."),
    "mc_flex_summary": ("Liquid-fuel droplet combustion. A bounded 17-record Table IX sample, not the complete FLEX investigation.", "Горение жидких капель. Ограниченная выборка из 17 записей таблицы IX, а не полное исследование FLEX."),
    "mc_bass_summary": ("Thin solid PMMA, opposed-flow flame extinction. Two oxygen conditions and three distinct evidence methods.", "Тонкий твёрдый PMMA, затухание пламени во встречном потоке. Два кислородных условия и три различных метода получения результатов."),
    "mc_method_cells": ("Published method cells", "Опубликованных значений методов"),
    "mc_bass_not_tests": ("Six method-specific cells are not six independent experiments.", "Шесть результатов по методам не являются шестью независимыми испытаниями."),
    "mc_workflow": ("Explore source evidence → search records → verify eligible claims → export a separate evidence ledger.", "Изучите источники → найдите записи → проверьте допустимые утверждения → экспортируйте отдельный журнал доказательств."),
    "mc_restriction": ("Not a fire simulator, safety threshold estimator, or Moon/Mars prediction system. Independent counterexample search is not implemented.", "Это не симулятор пожара, не оценщик безопасных порогов и не система прогнозов для Луны/Марса. Независимый поиск контрпримеров не реализован."),
    "mc_flex_tab": ("FLEX · droplets", "FLEX · капли"),
    "mc_bass_tab": ("BASS-II · solids", "BASS-II · твёрдое топливо"),
    "mc_ledger_heading": ("Session Evidence Ledgers", "Журналы доказательств текущей сессии"),
    "mc_ledger_intro": ("FLEX and BASS-II are exported separately. History is session-only until JSON export.", "FLEX и BASS-II экспортируются раздельно. До сохранения JSON история доступна только в текущей сессии."),
    "mc_methods_heading": ("Methods, provenance & limitations", "Методы, источники и ограничения"),
    "mc_methods_dap": ("NASA-DAP D0–D7 tracks source identity, raw values, locators, quality checks and versioned releases.", "NASA-DAP D0–D7 обеспечивает идентификацию источника, сохранение исходных значений, локаторы, контроль качества и версионирование релизов."),
    "mc_methods_evp": ("NASA-EVP checks structured claims independently; SUPPORTED means source transcription within scope, not physical or safety certification.", "NASA-EVP независимо проверяет структурированные утверждения; SUPPORTED означает подтверждение источником в заданных пределах, а не сертификацию физической или пожарной безопасности."),
    "mc_methods_limit": ("English claim parsing is intentionally restricted. LLM synthesis, unrestricted reasoning and automated counterexample search are not included in this release.", "Английский парсер намеренно ограничен. В этом релизе нет LLM-синтеза, неограниченного научного рассуждения или автоматического поиска контрпримеров."),
    "language": ("Interface language", "Язык интерфейса"),
    "tagline": ("Stellar Anvil | NASA Space Apps Challenge 2026", "Stellar Anvil | NASA Space Apps Challenge 2026"),
    "explorer": ("NASA Evidence Explorer — FLEX", "Обзор научных данных NASA — FLEX"),
    "load_failed": ("FLEX D7 release validation failed. No data displayed.", "Ошибка проверки релиза FLEX D7. Данные не отображаются."),
    "source_records": ("Source-linked records", "Записей с источниками"),
    "verified_lookup": ("Verified for point lookup", "Проверено для просмотра записей"),
    "needs_review": ("Require review", "Требуют дополнительной проверки"),
    "data_release": ("Data release: {id} | NASA/TP-2015-216046, Table IX", "Релиз данных: {id} | NASA/TP-2015-216046, таблица IX"),
    "bounded_warning": ("This is a bounded, read-only scientific sample. QC status does not establish causal relationships, safety thresholds, or predictions.", "Это ограниченная научная выборка, доступная только для чтения. Статус QC не доказывает причинные связи, пороги безопасности или прогнозы."),
    "filter_heading": ("Filter experiments", "Фильтр экспериментов"),
    "search_id": ("Search by experiment ID", "Поиск по идентификатору опыта"),
    "id_example": ("e.g. FLEX-034", "например, FLEX-034"),
    "fuel": ("Fuel", "Топливо"),
    "oxygen_norm": ("O₂ mole fraction (normalized)", "Мольная доля O₂ (нормализованная)"),
    "normalized_help": ("Uses audited normalized text for filtering. Original NASA strings remain unchanged.", "Для фильтрации используются проверенные нормализованные записи. Исходные строки NASA не изменяются."),
    "test_end": ("Reported test end", "Зарегистрированный исход опыта"),
    "d4_status": ("D4 QC status", "Статус D4 QC (контроль данных)"),
    "filter_count": ("Showing {selected} of {total} audited FLEX records. Empty filter selections mean 'all'.", "Показано {selected} из {total} проверенных записей FLEX. Пустой выбор фильтра означает «все»."),
    "test_id": ("Test ID", "ID опыта"),
    "fuel_raw": ("Fuel (raw)", "Топливо (исходное значение)"),
    "oxygen_raw": ("O₂ mole fraction (raw)", "Мольная доля O₂ (исходное значение)"),
    "pressure_raw": ("Pressure (raw, mmHg)", "Давление (исходное, mmHg)"),
    "extinction_raw": ("Droplet diameter at visible flame extinction (raw, mm)", "Диаметр капли при исчезновении видимого пламени (исходный, mm)"),
    "source_locator": ("NASA source locator", "Локатор источника NASA"),
    "empty_filter": ("No experiments match the selected filters. Try changing or clearing your selections.", "Ни один опыт не соответствует фильтрам. Измените или очистите условия."),
    "composition": ("Audited sample composition", "Состав проверенной выборки"),
    "composition_warning": ("Categorical counts for {selected} of {total} selected FLEX D7 records ({id}). These counts do not represent all FLEX tests. No causal comparisons or physical predictions are implied.", "Число записей по категориям: {selected} из {total} записей FLEX D7 ({id}). Выборка не представляет все испытания FLEX; причинные сравнения и физические прогнозы не допускаются."),
    "audited_records": ("Audited records", "Проверенные записи"),
    "chart_end_title": ("Test outcome", "Исход опыта"),
    "chart_qc_title": ("D4 QC status", "D4 QC: статус"),
    "chart_end_completion": ("Completion", "Завершение"),
    "chart_end_disruption": ("Disruption", "Разрушение капли"),
    "bass_title": ("BASS-II — Table 2.1 Evidence Card", "BASS-II — Карточка свидетельств, таблица 2.1"),
    "bass_intro": ("Six published method-specific results in two nominal oxygen conditions; {release}. Thin PMMA, 1 atm, opposed flow, ISS microgravity. NASA/TM-20210011385, printed p.28 / PDF p.36.", "Шесть опубликованных результатов по трём методам и двум номинальным условиям O₂; {release}. Тонкий PMMA, 1 atm, встречный поток, микрогравитация МКС. NASA/TM-20210011385, печатная с.28 / PDF с.36."),
    "bass_report": ("Original NASA report", "Оригинальный отчёт NASA"),
    "bass_condition": ("Nominal oxygen condition", "Номинальное содержание кислорода"),
    "bass_all": ("Both conditions (6 method cells)", "Оба условия (6 значений методов)"),
    "bass_o2": ("Nominal O₂", "Номинальный O₂"),
    "bass_method": ("Evidence method", "Метод получения результата"),
    "bass_kind": ("Evidence kind", "Тип результата"),
    "bass_velocity": ("Critical opposed-flow gas velocity, Vg,cr", "Критическая скорость встречного газового потока, Vg,cr"),
    "bass_uncertainty": ("Reported uncertainty", "Опубликованная неопределённость"),
    "bass_method_experiment": ("Experiment", "Эксперимент"),
    "bass_method_computation": ("Computation", "Численная модель"),
    "bass_method_theory": ("Theory, Equation (2.5)", "Теория, уравнение (2.5)"),
    "bass_not_reported": ("Not reported", "Не сообщена"),
    "bass_method_warning": ("These are two published oxygen-condition rows and three distinct methods, not six independent experiments. Experimental ±5 mm/s is reported with unspecified statistical basis; model uncertainties are not reported (not zero).", "Это две строки по условиям O₂ и три разных метода, а не шесть независимых испытаний. Экспериментальное ±5 mm/s опубликовано без указания статистической природы; неопределённости моделей не сообщены (это не ноль)."),
    "bass_discrepancy": ("Unresolved source discrepancy: Table 2.1 reports 30±5 mm/s at 16% O₂, while Section 2.2.5 discusses approximately 26 and 40 mm/s for differing sample widths/thicknesses; their mapping is not established.", "Неразрешённое расхождение источника: таблица 2.1 содержит 30±5 mm/s при 16% O₂, а раздел 2.2.5 описывает приблизительно 26 и 40 mm/s при различной ширине/толщине образцов; соответствие не установлено."),
    "bass_scope": ("Restricted reported outputs only. No unique as-run test IDs, oxygen-only causal proof, general safe airflow threshold, Moon/Mars prediction, or quantitative pooling with FLEX droplets.", "Только ограниченные опубликованные результаты. Нет однозначных ID отдельных испытаний, доказанной кислородной причинности, общего порога безопасного потока, прогнозов для Луны/Марса или объединения физических величин с каплями FLEX."),
    "bass_no_evp": ("This evidence card displays D7 source cells only. Use Verify → BASS-II for structured source-cell verdicts; it does not certify physical safety.", "Эта карточка показывает только исходные ячейки D7. Для проверки отдельного утверждения перейдите в раздел «Проверка → BASS-II»; он не сертифицирует физическую безопасность."),
    "bass_provenance": ("Exact NASA locators and QC restrictions", "Точные локаторы NASA и ограничения QC"),
    "bass_original_id_note": ("Empty original_test_id is intentional: Table 2.1 was not uniquely matched to Appendix A.1 runs.", "Пустой original_test_id оставлен намеренно: строки таблицы 2.1 не сопоставлены однозначно с испытаниями приложения A.1."),
    "bass_load_error": ("BASS-II D7 integrity failed; no BASS-II results displayed. FLEX is unaffected.", "Не пройдена проверка целостности BASS-II D7; его данные не показаны. FLEX не затронут."),

    "bass_verify_title": ("BASS-II — Verify a Table 2.1 source cell", "BASS-II — Проверка ячейки таблицы 2.1"),
    "bass_verify_intro": ("Structured source transcription only. Select one of six method-specific cells, enter the asserted value including ± if published, and verify it against fresh D7. No free-text or safety prediction.", "Только проверка исходной ячейки. Выберите одно из шести значений с указанием метода, введите проверяемое значение (включая ±, если опубликовано) и выполните проверку по D7. Свободный текст и прогноз безопасности не поддерживаются."),
    "bass_verify_cell": ("Published source cell (condition + method)", "Исходная ячейка (условие + метод)"),
    "bass_verify_example": ("e.g. 10±5, 15, or 1±0.5", "например, 10±5, 15 или 1±0.5"),
    "bass_verify_button": ("Verify BASS-II source claim", "Проверить утверждение BASS-II"),
    "bass_verify_supported": ("Matches the published method-specific cell; not independent physical validation.", "Совпадает с опубликованной ячейкой выбранного метода; не подтверждает физическую достоверность независимо."),
    "bass_verify_contradicted": ("The number, published uncertainty, or converted unit differs from this source cell.", "Число, опубликованная неопределённость или преобразованная единица не совпадают с ячейкой источника."),
    "bass_verify_error": ("Technical source verification failed; no scientific verdict.", "Технический сбой проверки источника; научный вердикт не присвоен."),
    "bass_verify_no_asrun": ("Table 2.1 does not identify a unique original test ID. Methods are not independent experiments.", "Таблица 2.1 не устанавливает уникальный ID отдельного испытания; три метода не являются независимыми опытами."),
    "bass_verify_ledger": ("BASS-II Session Evidence Ledger", "Журнал доказательств BASS-II"),
    "bass_verify_ledger_note": ("Separate from the FLEX ledger. This session-only JSON records actual BASS-II structured checks and limitations. Export to preserve it.", "Отдельно от журнала FLEX. Этот JSON текущей сессии хранит выполненные структурированные проверки BASS-II и ограничения. Выгрузите его для сохранения."),
    "bass_verify_download": ("Download BASS-II Evidence Ledger (JSON)", "Скачать журнал BASS-II (JSON)"),
    "chart_end_extinction": ("Extinction", "Исчезновение пламени"),
    "inspect_record": ("Inspect a source record", "Просмотр исходной записи"),
    "experiment_id": ("Experiment ID", "ID эксперимента"),
    "review_warning": ("D4 REVIEW — unresolved source or interpretation limitations apply.", "D4 REVIEW — имеются неразрешённые ограничения источника или интерпретации."),
    "verified_warning": ("D4 VERIFIED — only limited source-point lookup and display are permitted.", "D4 VERIFIED — разрешён только ограниченный просмотр данных источника; научный вывод не подтверждён автоматически."),
    "source_anchor": ("Source locator", "Локатор источника"),
    "original_report": ("Original NASA report", "Оригинальный отчёт NASA"),
    "figure_locator": ("Appendix B / figure locator", "Локатор приложения B / рисунка"),
    "not_recorded": ("Not recorded", "Не указано"),
    "none_recorded": ("None recorded", "Не зафиксировано"),
    "permitted_uses": ("Permitted uses", "Разрешённое использование"),
    "blocked_uses": ("Blocked uses", "Запрещённое использование"),
    "qc_flags": ("QC flags", "Флаги контроля качества (QC)"),
    "review_reason": ("Review reason", "Причина дополнительной проверки"),
    "field_limits": ("Field-level restrictions and raw value preservation", "Ограничения полей и сохранение исходных значений"),
    "pressure_field": ("Pressure (raw mmHg)", "Давление (исходное, mmHg)"),
    "extinction_field": ("Extinction droplet diameter (raw mm)", "Диаметр капли при исчезновении пламени (исходный, mm)"),
    "blocked": ("Blocked", "Заблокировано"),
    "curated_text": ("Curated text", "Проверенный текст"),
    "quoted_note": ("Quoted values distinguish literal '0', missing '–', and empty ''.", "Значения в кавычках различают буквальный «0», пропуск «–» и пустую строку «»."),
    "raw_row": ("Original NASA Table IX row — unchanged strings", "Строка исходной таблицы NASA IX — строки не изменены"),
    "evidence_search": ("Evidence Search — FLEX D7", "Поиск научных свидетельств — FLEX D7"),
    "search_help": ("Literal keyword search through 17 audited records. All terms must match one record. Ranking measures lexical relevance, not scientific confidence or verification.", "Буквальный поиск по 17 аудированным записям: вводите исходные английские значения или ID. Все слова запроса должны встретиться в одной записи. Рейтинг оценивает текстовую релевантность, а не научную достоверность."),
    "search_meta": ("Search experiment and QC metadata", "Поиск по данным опытов и QC"),
    "search_placeholder": ("e.g. FLEX-034 or Heptane VERIFIED", "например, FLEX-034 или Heptane VERIFIED"),
    "search_intro": ("Enter one or more terms to inspect NASA-linked records.", "Введите одно или несколько ключевых слов для поиска записей NASA."),
    "search_empty": ("No matching records in this bounded FLEX D7 release.", "В ограниченном релизе FLEX D7 совпадений не найдено."),
    "search_count": ("{count} matching record(s) of {total} in {id}.", "Найдено {count} из {total} записей релиза {id}."),
    "rank": ("Rank", "Место"),
    "outcome": ("Reported outcome", "Исход опыта"),
    "lexical_score": ("Lexical score", "Текстовый рейтинг"),
    "why_matched": ("Why matched", "Почему найдено"),
    "d4_qc": ("D4 QC", "D4 QC"),
    "rank_caveat": ("Lexical scores are search weights, not reliability, risk, physical performance, or NASA-EVP verdicts.", "Текстовый рейтинг отражает только совпадение запроса, а не надёжность, риск, физические характеристики или вердикт NASA-EVP."),
    "inspect_ranked": ("Inspect ranked result", "Просмотр результата поиска"),
    "d4_review_detail": ("D4 REVIEW — source restrictions apply.", "D4 REVIEW — действуют ограничения источника."),
    "d4_verified_detail": ("D4 VERIFIED — limited point lookup only.", "D4 VERIFIED — только ограниченный просмотр записи."),
    "ranking_explanation": ("Ranking explanation", "Объяснение ранжирования"),
    "table_reference": ("Table IX reference", "Ссылка на таблицу IX"),
    "printed_pdf": ("printed p.{printed}; PDF p.{pdf}", "печатная с.{printed}; PDF с.{pdf}"),
    "source_qc_expander": ("Source values and QC restrictions", "Исходные значения и ограничения QC"),
    "oxygen_source": ("Oxygen mole fraction (raw; dimensionless)", "Мольная доля O₂ (исходная; безразмерная)"),
    "ambient_source": ("Ambient pressure (raw; mmHg)", "Давление среды (исходное; mmHg)"),
    "visible_source": ("Droplet diameter at visible-flame extinction (raw; mm)", "Диаметр капли при исчезновении видимого пламени (исходный; mm)"),
    "audited_figure": ("Audited figure locator", "Локатор проверенного рисунка"),
    "verification": ("Evidence Verification — FLEX D7", "Проверка научных утверждений — FLEX D7"),
    "verification_intro": ("Verify source-linked structured claims against NASA/TP-2015-216046, Table IX. This 17-record sample is not a predictive dataset. English parsing supports only a restricted grammar; no automatic counterexample search.", "Проверка структурированных утверждений по NASA/TP-2015-216046, таблица IX. Выборка из 17 записей не подходит для прогнозов. Английский парсер поддерживает только ограниченные формулировки; автоматического поиска контрпримеров нет."),
    "nasa_id": ("NASA experiment ID", "ID опыта NASA"),
    "claim_class": ("Claim class", "Класс утверждения"),
    "reported_field": ("Reported Table IX field", "Поле из таблицы IX"),
    "asserted_value": ("Asserted value", "Заявленное значение"),
    "value_placeholder": ("Example: 0.21 or 0.34", "Пример: 0.21 или 0.34"),
    "asserted_unit": ("Asserted unit", "Единица заявленного значения"),
    "scope_notice": ("This is a declared scope class, not an automatic interpretation of free text.", "Класс области применимости выбирается вручную; текст утверждения автоматически не интерпретируется."),
    "verify_button": ("Verify structured claim", "Проверить структурированное утверждение"),
    "latest_verification": ("Latest observed verification", "Последняя выполненная проверка"),
    "evaluated_claim": ("Evaluated claim: {desc}", "Проверенное утверждение: {desc}"),
    "confirmed_english": ("Confirmed English statement", "Подтверждённое английское утверждение"),
    "asserted": ("Asserted", "Заявлено"),
    "technical_error": ("Technical ERROR — no scientific verdict.", "Технический ERROR — научный вердикт не присвоен."),
    "verifier_note": ("Scientific explanation", "Объяснение научного вердикта"),
    "verifier_original": ("Original verifier explanation (English, unchanged)", "Оригинальное объяснение verifier (английский, без изменений)"),
    "source_raw_value": ("Source raw value", "Исходное значение NASA"),
    "source_unit": ("Source unit", "Единица в источнике"),
    "not_applicable": ("Not applicable", "Не применяется"),
    "source_qc_status": ("D4 QC status", "Статус качества D4 QC"),
    "physical_block": ("Field-level numerical physical use is blocked by the D7 audit.", "Числовое использование этого поля для физического анализа запрещено аудитом D7."),
    "proof_expander": ("Proof checks and full verifier output", "Проверки доказательств и полный вывод verifier"),
    "check": ("Check", "Проверка"),
    "result": ("Result", "Результат"),
    "ledger": ("Session Evidence Ledger", "Журнал доказательств текущей сессии"),
    "ledger_caveat": ("This ledger exists only in this Streamlit session. Export JSON to preserve observed checks. No source CSV is changed.", "Журнал хранится только в текущей сессии Streamlit. Выгрузите JSON для сохранения проверок. Исходные CSV не изменяются."),
    "entry": ("Entry", "Запись"),
    "experiment": ("Experiment", "Эксперимент"),
    "class": ("Class", "Класс"),
    "verdict": ("Verdict", "Вердикт"),
    "technical": ("Technical", "Технический статус"),
    "download_ledger": ("Download Evidence Ledger (JSON)", "Скачать журнал доказательств (JSON)"),
    "ledger_empty": ("No claims evaluated in this session yet.", "В этой сессии ещё не выполнено проверок."),
    "english_expander": ("English Table IX statement — constrained input", "Английское утверждение Table IX — ограниченный ввод"),
    "english_help": ("Only a narrow English grammar for one Table IX source cell is supported. Parsing is not verification. Confirm extracted fields before NASA-EVP.", "Поддерживаются только ограниченные английские шаблоны об одной ячейке таблицы IX. Разбор текста не является проверкой. Подтвердите извлечённые поля перед NASA-EVP."),
    "english_label": ("Enter one English Table IX statement", "Введите одно утверждение на английском языке (русский парсер недоступен)"),
    "english_example": ("NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002.", "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002."),
    "parse_button": ("Parse statement", "Разобрать утверждение"),
    "text_changed": ("Text changed. Parse again to inspect the updated statement.", "Текст изменился. Повторите разбор, чтобы проверить новые поля."),
    "candidate_only": ("Candidate only — not yet scientifically verified", "Кандидат утверждения — научная проверка ещё не выполнена"),
    "confirm_button": ("Confirm parsed fields and verify", "Подтвердить поля и проверить"),
    "confirm_success": ("Confirmed claim evaluated. See verdict and ledger below.", "Подтверждённое утверждение проверено. Вердикт и журнал показаны ниже."),
    "parse_error": ("Parsing failed", "Не удалось разобрать утверждение"),
    "scope_policy": ("scope policy", "правило области применимости"),
    "not_in_release": ("Not recorded in this release", "Не указано в этом релизе"),
    "source_note_english": ("D7/source note in English (unchanged)", "Оригинальная заметка D7 на английском (без изменений)"),
    "ranking_source": ("Original ranking reasons", "Исходные причины ранжирования"),
}

TRANSLATIONS = {
    lang: {key: values[index] for key, values in _TRANSLATIONS.items()}
    for index, lang in enumerate(LANGUAGES)
}

CODE_DESCRIPTIONS = {
    "VERIFIED": "Проверено для ограниченного просмотра (D4)",
    "REVIEW": "Требует проверки (D4)",
    "SUPPORTED": "Подтверждено источником (NASA-EVP)",
    "CONTRADICTED": "Противоречит источнику (NASA-EVP)",
    "INSUFFICIENT_EVIDENCE": "Недостаточно доказательств (NASA-EVP)",
    "OUT_OF_SCOPE": "За пределами применимости (NASA-EVP)",
    "ERROR": "Техническая ошибка, не вердикт",
    "Disruption": "Разрушение капли",
    "Extinction": "Исчезновение видимого пламени",
    "Completion": "Завершение испытания",
    "Methanol": "Метанол",
    "Heptane": "Гептан",
    "SOURCE_TRANSCRIPTION": "Буквальная запись источника",
    "LIMITED_REPORTED_VALUE": "Сообщённое значение с ограничениями QC",
    "CAUSAL_EFFECT": "Причинный эффект",
    "EXPERIMENTAL_THRESHOLD": "Экспериментальный порог",
    "MOON_MARS_EXTRAPOLATION": "Перенос на Луну/Марс",
    "CERTIFIED_SAFE": "Подтверждённая безопасность",
    "FIRE_RISK_SCORE": "Оценка пожарного риска",
}

FIELD_DESCRIPTIONS = {
    "fuel_raw": "Топливо (категория)",
    "oxygen_mole_fraction_raw": "Мольная доля O₂",
    "initial_droplet_diameter_mm_raw": "Начальный диаметр капли",
    "visible_flame_extinction_diameter_mm_raw": "Диаметр капли при исчезновении видимого пламени",
    "ambient_pressure_mmhg_raw": "Давление среды",
    "burning_rate_mm2_per_s_raw": "Средний коэффициент скорости горения",
    "burn_time_s_raw": "Время горения",
    "flex_test_id": "ID опыта",
    "qc_dap_d4_record_status": "Статус D4 QC",
    "qc_review_reason": "Причина проверки QC",
    "qc_permitted_uses": "Разрешённое использование",
    "qc_blocked_uses": "Запрещённое использование",
    "qc_qc_flags": "Флаги QC",
    "curated_oxygen_mole_fraction": "Нормализованная мольная доля O₂",
}

# Source-generated English notes are matched exactly. Unrecognized source text
# is shown verbatim rather than subjected to guesswork or translation APIs.
SOURCE_NOTE_RU = {
    "Visible extinction diameter = 0.89 mm while test end is Disruption; do not infer measurement order or that disruption occurred at 0.89 mm.": "Указан диаметр капли 0.89 mm при исходе Disruption (разрушение); нельзя утверждать, что разрушение произошло именно при 0.89 mm или в определённом порядке событий.",
    "Basic source/schema/range checks pass for this record; this does not validate a cross-test physical claim.": "Проверены исходная запись, схема и допустимые диапазоны; межэкспериментальный физический вывод этим не подтверждён.",
    "NONE — figure-caption limitations remain attached to the record": "Отдельная причина не указана; ограничения подписей к рисункам продолжают действовать.",
    "Test end is Extinction but diameter field is an em dash. Report A.1 mentions out-of-view/no reliable extrapolation as one possible reason; not proven for this test.": "Итог испытания — Extinction, но поле диаметра содержит пропуск «–». В приложении A.1 упомянута возможная причина, но для этого опыта она не доказана.",
    "GMT time and four numeric test fields are em dashes (droplet diameter, extinction diameter, burning rate, burn time).": "Время GMT и четыре числовых поля указаны как пропуски «–»: диаметр капли, диаметр при исчезновении пламени, скорость горения и время горения.",
    "Test end = Completion but a positive visible extinction diameter (1.56 mm) appears; semantics unresolved.": "Исход — Completion (завершение), хотя поле диаметра при исчезновении видимого пламени содержит 1.56 mm. Значение этого сочетания не установлено.",
    "Table IX (printed p21) lists 2 mm extinction diameter; Figure 38 caption (printed p62) explicitly says no extinction droplet diameter is reported. Source discrepancy not resolved.": "В таблице IX на печатной с.21 указано 2 mm, но подпись к рисунку 38 на с.62 сообщает, что диаметр капли при исчезновении пламени не определён. Противоречие не разрешено.",
    "Literal 0 mm appears in extinction diameter field with Disruption outcome. Preserve zero; do not treat it as measurement of zero-size flame or a missing mark.": "В ячейке диаметра при исчезновении пламени указан буквальный 0 mm при исходе Disruption. Это не измерение «пламени нулевого размера» и не пропуск.",
    "Basic source/schema/range checks pass for this record; no cross-test causal conclusions.": "Базовые проверки источника, схемы и диапазонов пройдены; причинные выводы по разным опытам не разрешены.",
    "Literal 0 mmHg absolute ambient pressure conflicts with an ordinary positive-pressure combustion test. Source correction unavailable; do not substitute another pressure.": "В источнике указан 0 mmHg абсолютного давления — аномалия для данного испытания. Исправление источника отсутствует; нельзя подставлять другое давление.",
    "Causal or extinction-only trend based on recorded extinction diameter": "Запрещён причинный анализ или тренд исключительно по указанному диаметру при исчезновении пламени.",
    "Uncontrolled comparisons without fuel/support/method matching": "Запрещены неконтролируемые сравнения без согласования топлива, подвеса и метода измерения.",
    "Cross-test causal/comparative physical conclusions; direct flame-diameter inference from extinction droplet diameter": "Запрещены причинные и прямые количественные сравнения между опытами; диаметр капли нельзя считать диаметром пламени.",
    "Extinction-diameter numerical use": "Числовое использование диаметра капли при исчезновении пламени запрещено.",
    "Numerical droplet or burn-rate analysis": "Запрещён числовой анализ диаметра капли и коэффициента скорости горения для этих пропущенных полей.",
    "Extinction-only physical inference using the value": "Запрещено делать физический вывод только по указанному диаметру при исчезновении пламени.",
    "Extinction-diameter numeric interpretation; causal/trend inference from this value": "Запрещены количественная интерпретация указанного диаметра и причинный/трендовый вывод из него.",
    "Pressure-based calculations; comparisons requiring pressure": "Запрещены расчёты по давлению и сравнения, требующие корректного давления.",
    "Exact source lookup, categorical outcome display": "Разрешены точный просмотр первоисточника и показ категории исхода.",
    "Exact source lookup, point-level display": "Разрешены точный просмотр первоисточника и отображение отдельной записи.",
    "Source-linked point lookup; reported Table IX cells with figure-caption caveats": "Разрешён просмотр записи с указанием источника и значений таблицы IX с оговорками подписей к рисункам.",
    "Exact source lookup, remaining nonmissing point fields": "Разрешены точный просмотр источника и отображение остальных полей, в которых нет пропусков.",
    "Metadata/fuel/ambient settings/outcome display": "Разрешён показ метаданных, топлива, условий среды и исхода опыта.",
    "Exact source lookup, raw reported values with caution": "Разрешён точный просмотр и исходных значений с оговорками.",
    "Exact source lookup; show raw Table IX value and Figure 38 warning": "Разрешён показ исходного значения Table IX с предупреждением о Figure 38.",
    "Exact source lookup; raw value shown with anomaly flag": "Разрешён просмотр исходного значения с указанием флага аномалии.",
}

QC_FLAGS_RU = {
    "NONE": "Отдельные флаги отсутствуют",
    "OUTCOME_DIAMETER_REVIEW": "Нужна проверка соответствия исхода и диаметра",
    "LLUV_CALIBRATION_LOW_CONTRAST": "Калибровка LLUV: низкий контраст",
    "EXTINCTION_DIAMETER_UNAVAILABLE": "Диаметр при исчезновении видимого пламени недоступен",
    "LLUV_INCOMPLETE_CALIBRATION_POSSIBLE_BUBBLE": "Неполная калибровка LLUV; возможен пузырёк",
    "HIBMS_FOV_INTERRUPTION_LLUV_DIM": "Прерывание области наблюдения HIBMS; слабый сигнал LLUV",
    "MISSING_TIME_AND_FOUR_METRICS": "Отсутствуют время и четыре измеряемых поля",
    "COMPLETION_WITH_POSITIVE_EXTINCTION_DIAMETER": "Исход Completion при положительном диаметре исчезновения пламени",
    "COLOR_CAMERA_MISSING": "Отсутствует запись цветной камеры",
    "TABLE_CAPTION_EXTINCTION_DIAMETER_CONTRADICTION": "Противоречие таблицы и подписи рисунка по диаметру",
    "CAPTION_INDICATES_POST_VISIBLE_EXTINCTION_COOL_FLAME": "Подпись описывает холодное пламя после исчезновения видимого пламени",
    "ZERO_EXTINCTION_DIAMETER_WITH_DISRUPTION": "Буквальный ноль диаметра при исходе Disruption",
    "VERY_DIM_FLAME_IN_LLUV_AND_COLOR": "Очень слабое пламя по LLUV и цветной камере",
    "ZERO_AMBIENT_PRESSURE_BLOCK": "Аномальное нулевое давление; числовой анализ заблокирован",
}

PARSER_REASONS_RU = {
    "Text is required.": "Введите текст утверждения.",
    "Provide one short Table IX claim.": "Введите одно короткое утверждение о Table IX.",
    "Ambiguous matching grammar.": "Неоднозначное соответствие шаблону; уточните фразу.",
    "Only a single explicitly attributed Table IX source-cell statement is supported; no causal or physical-validity claims.": "Поддерживается только одно утверждение о буквальном содержимом ячейки Table IX; причинные выводы и физическая достоверность не проверяются.",
    "Missing D7 identity/locator fields.": "Отсутствуют ID опыта или локатор в D7.",
    "Exactly one D7 record is required for this experiment ID.": "Для этого ID должна существовать ровно одна запись D7.",
    "No source anchor for this record.": "У записи отсутствует локатор источника.",
    "Candidate parsed; not verified. Confirm fields before evaluation.": "Кандидат разобран, но ещё не проверен. Подтвердите поля.",
}

SCOPE_EXPLANATIONS_RU = {
    "No controlled comparability review supports a causal effect across these selected records.": "Для выбранных записей не установлена достаточная сопоставимость опытов, чтобы подтверждать причинный эффект.",
    "The selected records do not establish a validated general experimental threshold.": "Выбранные записи не устанавливают проверенный общий экспериментальный порог.",
    "FLEX ISS microgravity records cannot validate partial-gravity predictions.": "Данные FLEX с МКС не подтверждают прогнозы для частичной гравитации Луны или Марса.",
    "These FLEX droplet experiments cannot certify spacecraft materials or hardware as fire safe.": "Опыты FLEX с каплями не позволяют сертифицировать материалы или оборудование по пожарной безопасности.",
    "This release does not provide validated fire-risk scores or safety ratings.": "Релиз не содержит валидированной модели пожарного риска или рейтинга безопасности.",
}

VERDICT_SUMMARY_RU = {
    "SUPPORTED": "Для заявленного класса утверждения проверка источника и применимых условий прошла. Это не независимое подтверждение физических закономерностей.",
    "CONTRADICTED": "Заявленное значение или единица измерения противоречит указанной записи источника в рамках данного класса утверждения.",
    "INSUFFICIENT_EVIDENCE": "Свидетельств недостаточно для подтверждения утверждения. Отсутствие подтверждения не означает физического опровержения.",
    "OUT_OF_SCOPE": "Утверждение выходит за область допустимого использования выбранной выборки NASA.",
    "ERROR": "Техническая ошибка проверки; научный вердикт не присваивается.",
}


def tr(key: str, language: str = "en", **kwargs: object) -> str:
    """Translate one stable UI key; fail loudly for absent translations."""
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported interface language: {language}")
    try:
        pattern = TRANSLATIONS[language][key]
    except KeyError as exc:
        raise KeyError(f"Missing UI translation: {language}.{key}") from exc
    return pattern.format(**kwargs)


def init_language(state: MutableMapping[str, object]) -> str:
    """Initialize the UI preference only; do not touch other session keys."""
    if state.get(LANGUAGE_KEY) not in LANGUAGES:
        state[LANGUAGE_KEY] = "en"
    return str(state[LANGUAGE_KEY])


def change_language(state: MutableMapping[str, object], language: str) -> str:
    """Change the locale without resetting filters, claims, or ledger."""
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported interface language: {language}")
    state[LANGUAGE_KEY] = language
    return language


def display_code(value: str, language: str) -> str:
    """Codes and NASA raw categorical values stay visible in both modes."""
    if language == "ru" and value in CODE_DESCRIPTIONS:
        return f"{value} — {CODE_DESCRIPTIONS[value]}"
    return value


def field_label(field: str, language: str, english: str | None = None) -> str:
    if language == "ru":
        return FIELD_DESCRIPTIONS.get(field, english or field)
    return english or field


def source_note(note: str, language: str) -> str:
    """Exact-match presentation translation, never edits the stored note."""
    if language == "ru":
        return SOURCE_NOTE_RU.get(note, note)
    return note


def qc_flags_text(flags: str, language: str) -> str:
    """Add translations without changing or suppressing the original QC codes."""
    if language != "ru":
        return flags
    return "; ".join(
        f"{flag} — {QC_FLAGS_RU[flag]}" if flag in QC_FLAGS_RU else flag
        for flag in flags.split(";")
    )


def parser_reason(reason: str, language: str) -> str:
    if language == "ru":
        return PARSER_REASONS_RU.get(reason, reason)
    return reason


def verifier_summary(result: dict, language: str) -> str:
    """Limited human-readable explanation, not a replacement for raw proof."""
    original = str(result.get("explanation") or "")
    if language != "ru":
        return original
    exact = SCOPE_EXPLANATIONS_RU.get(original)
    if exact is not None:
        return exact
    verdict = "ERROR" if result.get("technical_state") == "ERROR" else result.get("verdict")
    summary = VERDICT_SUMMARY_RU.get(str(verdict), "Невозможно определить статус проверки.")
    if verdict == "CONTRADICTED" and result.get("source_raw_value") is not None:
        raw = result["source_raw_value"]
        claimed = result.get("asserted_value")
        source_unit = result.get("source_unit") or ""
        claimed_unit = result.get("asserted_unit") or ""
        summary += f" NASA Table IX: {raw} {source_unit}; заявлено: {claimed} {claimed_unit}."
    if result.get("field_blocked") is True:
        summary += " Данное числовое поле заблокировано аудитом D7."
    return summary


def ranking_reason(reason: str, language: str) -> str:
    """Translate lexical explanation syntax; leave tokens/weights untouched."""
    if language != "ru":
        return reason
    parts = []
    for part in reason.split(" | "):
        match = re.fullmatch(r"(.+?): ([a-z0-9_]+) \((exact|substring); \+(\d+)\)", part)
        if match is None:
            parts.append(part)
            continue
        token, field, kind, score = match.groups()
        kind_ru = "точное совпадение" if kind == "exact" else "вхождение"
        parts.append(f"{token}: {field_label(field, language)} ({kind_ru}; +{score})")
    return " | ".join(parts)
