from itertools import zip_longest
def calc(admin, user):
    admin_answer = admin
    user_answer = user

    f_admin_answer = [sent.strip().split() for sent in admin_answer.strip().split('.') if sent]
    f_user_answer = [sent.strip().split() for sent in user_answer.strip().split('.') if sent]

    scores = []
    for pi, i in enumerate(f_admin_answer):
        for j in f_user_answer[pi:]:
            t_score = 0 #score of each sentence
            for a, u in zip_longest(i, j):
                if a == u:
                    t_score += 1
            avg = (t_score / len(i)) #average score
            if  avg >= 0.5: #if true, the next sentence of admin is checked with the user's next sentence.
                scores.append(avg)
                break 
            else: #the user's next sentence is compared with the same admin's sentence.
                scores.append(avg)
    return (max(scores))