# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
- 自分で学習を実行したか（`executed_training_myself`）：はい / いいえ（実行できた範囲：　）
- 学習前：`format_rate` =　 / `content_rate` =　
- 学習後：`format_rate` =　 / `content_rate` =　
- 退行した質問：
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
- 学習で変わったこと・変わらなかったこと：

## 宿題

- 取り組んだレベル：基礎 
- 変えた設定やデータ：num_train_epochs from 20 to 5. warmup_steps was also lowered from 6 to 2 for the shorter run (warmup would otherwise be more than half of the 10 steps), so this is a second changed setting and the differences below may partly come from it. Everything else (seed, data, learning rate, lora_r, generation settings) was the same. The session was restarted between runs.
- 結果（比較表や数字）：
  Item	Original (epochs=20)	Changed (epochs=5)
  steps	40	10
  warmup_steps	6	2
  format_rate (before → after)	0.095 → 1.000	0.095 → 1.000
  content_rate (before → after)	0.000 → 0.905 (19/21)	0.000 → 0.714 (15/21)
  Final training loss	0.0141	1.304 (logged once, at step 10)
  Training time (s)	___ (not recorded; read from the section 4 output)	70
  Regressed questions	none	none
  Remaining failures	2 (both assertions without evidence)	6 (1 evasion, 1    assertion, 1 wrong answer text, 3 scoring artifacts)

  Comparison of the two result.json files (result_ep20.json, result_ep5.json):

  The config differs only in num_train_epochs (20 vs 5) and warmup_steps (6 vs 2). Library versions, model revision, seed and generation settings are identical, and the before-training scores are identical (0.095 / 0.000).
After training, format_rate is the same (1.000) in both runs, so the format is already learned with 10 steps and a loss of 1.3. Content_rate rises from 0.714 to 0.905.
  Looking at individual questions, the 20-epoch run fixed all six failures of the 5-epoch run: the evasion ("PDF 以外でも出せますか"), the question-echo answer, the three correct refusals that lacked the word "確認" (the model now writes the full training sentence "この FAQ には記載がありません。運営に確認が必要です。"), and the フィードバック assertion. It also broke two questions that the 5-epoch run got right ("成績はいつ出ますか" and "オフィスアワーは事前予約が必要ですか"), which now receive an FAQ fact with needs_review: false. So the net gain of 4 questions hides a loss of 2.
The section 6 classifications are identical in both runs (one asserted, two needs_review, plus the control).
- ファインチューニングが向く場面・向かない場面についての考察：Suitable: when the problem is the shape of the output. A 10-step LoRA run took format_rate from 0.095 to 1.000 even though the prompt already asked for the same format, and 40 steps made the wording of answers and refusals consistent. A fixed output format, tone or wording is the kind of thing a few examples teach reliably.
Not suitable by itself: when the model must know facts or judge whether a source supports an answer. Even with 40 steps and a loss of 0.014, the model answered 成績 with the deadline and 事前予約 with the office hours, and the longer run lost two questions the shorter run had right. More training made the model copy training sentences more reliably, which helps format but makes confident wrong answers look as tidy as correct ones. With only 14 training examples the model cannot learn the boundary of what the FAQ covers, and when the FAQ changes the model has to be retrained, whereas a retrieval step would just read the new FAQ.
