using System;

// Pure session state: clock is supplied by GameSession so edge cases can be tested.
public sealed class CompetitionRun
{
    public const double DurationSeconds = 600;
    public enum FinishReason { None, TimeExpired, AllSkipped, Finished }
    public bool Running { get; private set; }
    public int CurrentLevel { get; private set; }
    public FinishReason Reason { get; private set; }
    public int[] Outcomes { get; private set; } = new int[3];
    private int[] levelPoints = { 200, 300, 500 };
    public int TotalScore { get { int total=0; for(int i=0;i<3;i++) if(Outcomes[i]==1) total+=levelPoints[i]; return total; } }
    public int MaximumScore { get { return levelPoints[0]+levelPoints[1]+levelPoints[2]; } }
    public int PointsForLevel(int level) { return level>=0 && level<3 ? levelPoints[level] : 0; }
    public int EarnedPointsForLevel(int level) { return level>=0 && level<3 && Outcomes[level]==1 ? levelPoints[level] : 0; }
    private double deadline, remaining = DurationSeconds;
    public int SolvedCount { get { int n=0; foreach(int x in Outcomes) if(x==1) n++; return n; } }
    public int SkippedCount { get { int n=0; foreach(int x in Outcomes) if(x==2) n++; return n; } }
    public double Remaining(double now) { return Running ? Math.Max(0,deadline-now) : remaining; }
    public bool Start(double now, int[] points = null)
    {
        if (Running) return false;
        // Snapshot at Start so editing settings during a run cannot change earned points.
        if (points!=null && points.Length!=3) throw new ArgumentException("Exactly three level scores are required.");
        levelPoints = points==null ? new[]{200,300,500} : (int[])points.Clone();
        for(int i=0;i<3;i++) levelPoints[i]=Math.Max(0,levelPoints[i]);
        Outcomes=new int[3]; CurrentLevel=0; Reason=FinishReason.None;
        remaining=DurationSeconds; deadline=now+DurationSeconds; Running=true;
        return true;
    }
    public bool Tick(double now)
    {
        if (!Running) return false;
        if (Remaining(now)>0) return true;
        Finish(FinishReason.TimeExpired,now); return false;
    }
    public bool Solve(int level,double now)
    {
        if (!Tick(now) || level!=CurrentLevel || Outcomes[level]==2) return false;
        Outcomes[level]=1;
        if (level==2) Finish(FinishReason.Finished,now);
        return true;
    }
    public bool Advance(int level,bool skip,double now)
    {
        if (!Tick(now) || level!=CurrentLevel) return false;
        if (skip && Outcomes[level]==0) Outcomes[level]=2;
        if (Outcomes[level]==0) return false;
        if (level==2) Finish(SkippedCount==3 ? FinishReason.AllSkipped : FinishReason.Finished,now);
        else CurrentLevel++;
        return true;
    }
    void Finish(FinishReason reason,double now)
    { remaining=Remaining(now); Running=false; Reason=reason; }
}
