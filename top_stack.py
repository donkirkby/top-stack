from csv import DictReader
from datetime import datetime
from itertools import groupby
from operator import itemgetter

import matplotlib.pyplot as plt


def main():
    with open('post_votes.csv') as votes:
        rows = list(DictReader(votes))

    today = datetime.today()

    for (post_type, title), post_rows in groupby(rows,
                                                 itemgetter('postType',
                                                            'title')):
        summary = f'{post_type[0]}: {title[:35]}'
        dates = []
        scores = []
        score = 0
        for row in post_rows:
            event = row['event']
            if event in ('AcceptedByOriginator',
                         'Favorite',
                         'ApproveEditSuggestion'):
                continue
            if event == 'UpMod':
                score += 1
            else:
                assert event == 'DownMod', event
                score -= 1
            dates.append(datetime.strptime(row['creationDate'],
                                           "%Y-%m-%d %H:%M:%S"))
            scores.append(score)
        dates.append(today)
        scores.append(score)
        plt.plot(dates, scores, label=summary)
    plt.legend()
    plt.title('Top posts')
    plt.ylabel('Score')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()


main()
