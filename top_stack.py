from csv import DictReader
from datetime import datetime
from itertools import groupby
from operator import itemgetter

import matplotlib.pyplot as plt
from matplotlib.dates import date2num


def main():
    with open('post_votes.csv') as votes:
        rows = list(DictReader(votes))
    if __name__ == '__live_coding__':
        rows = rows[:10000:20]

    today = datetime.today()
    highlight_count = 0
    max_score = 0
    min_score = 0
    start_date = None

    for post_id, post_rows in groupby(rows, itemgetter('postId')):
        post_rows = list(post_rows)
        first_row = post_rows[0]
        score = 0
        creation_date = parse_date(first_row, 'creationDate')
        if start_date is None or creation_date < start_date:
            start_date = creation_date
        dates = [creation_date]
        scores = [score]
        for row in post_rows:
            event = row['event']
            if event in ('AcceptedByOriginator',
                         'Favorite',
                         'ApproveEditSuggestion',
                         'BountyStart',
                         'BountyClose',
                         'ModeratorReview',
                         'Undeletion'):
                continue
            if event == 'UpMod':
                score += 1
            else:
                assert event == 'DownMod', event
                score -= 1
            max_score = max(score, max_score)
            min_score = min(score, min_score)
            dates.append(parse_date(row, 'voteDate'))
            scores.append(score)

        row = first_row
        if row['currentRank'] in {'1', '2', '3'} or row['postId'] == '46216':
            summary = f'{row["postType"][0]}: {row["title"][:45]}'
            highlight_count += 1
            color = f'C{highlight_count}'
            alpha = None
        else:
            summary = None
            color = 'k'
            alpha = 0.07
        dates.append(today)
        scores.append(score)

        plt.plot(dates, scores, label=summary, color=color, alpha=alpha)

    axes = plt.gca()
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_bounds(min_score, max_score)
    axes.spines['bottom'].set_bounds(date2num(start_date), date2num(today))

    plt.legend()
    plt.title('My Top Posts')
    plt.ylabel('Score')
    plt.xlabel('Date')
    plt.tight_layout()

    plt.show()


def parse_date(row, field_name):
    return datetime.strptime(row[field_name], "%Y-%m-%d %H:%M:%S")


main()
