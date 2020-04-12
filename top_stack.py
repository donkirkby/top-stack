from csv import DictReader
from datetime import datetime
from itertools import groupby
from operator import itemgetter

import matplotlib.pyplot as plt


def main():
    with open('post_votes.csv') as votes:
        rows = list(DictReader(votes))
    if __name__ == '__live_coding__':
        rows = rows[:1000]

    today = datetime.today()
    highlight_count = 0

    for post_id, post_rows in groupby(rows, itemgetter('postId')):
        post_rows = list(post_rows)
        dates = []
        scores = []
        score = 0
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
            dates.append(datetime.strptime(row['creationDate'],
                                           "%Y-%m-%d %H:%M:%S"))
            scores.append(score)
        row = post_rows[0]
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
    plt.legend()
    plt.title('My Top Posts')
    plt.ylabel('Score')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()


main()
