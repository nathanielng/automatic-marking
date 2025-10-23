"use client"

import { useState } from 'react';
import { FileText, BookOpen, Upload, Loader2, Download, BarChart3 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ThemeToggle } from '@/components/theme-toggle';

interface Essay {
  name: string;
  content: string;
}

interface Rubric {
  name: string;
  content: string;
}

interface Feedback {
  name: string;
  feedback: string;
}

export default function Home() {
  const [essays, setEssays] = useState<Essay[]>([]);
  const [rubrics, setRubrics] = useState<Rubric[]>([]);
  const [feedbackGuidance, setFeedbackGuidance] = useState('');
  const [selectedRubric, setSelectedRubric] = useState('');
  const [feedbacks, setFeedbacks] = useState<Feedback[]>([]);
  const [classFeedback, setClassFeedback] = useState('');
  const [isMarking, setIsMarking] = useState(false);
  const [markingProgress, setMarkingProgress] = useState(0);
  const [markingStatus, setMarkingStatus] = useState('');
  const [selectedFeedback, setSelectedFeedback] = useState('');

  const handleEssaysUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const loadedEssays: Essay[] = [];
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const content = await file.text();
      loadedEssays.push({ name: file.name, content });
    }
    setEssays(loadedEssays);
  };

  const handleRubricsUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const loadedRubrics: Rubric[] = [];
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const content = await file.text();
      loadedRubrics.push({ name: file.name, content });
    }
    setRubrics(loadedRubrics);
  };

  const handleFeedbackGuidanceUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const content = await files[0].text();
    setFeedbackGuidance(content);
  };

  const startMarking = async () => {
    if (!selectedRubric || essays.length === 0 || !feedbackGuidance) {
      alert('Please upload essays, select a rubric, and upload feedback guidance first.');
      return;
    }

    setIsMarking(true);
    setMarkingProgress(0);
    setFeedbacks([]);
    setClassFeedback('');

    const rubric = rubrics.find(r => r.name === selectedRubric);
    if (!rubric) return;

    const generatedFeedbacks: Feedback[] = [];

    for (let i = 0; i < essays.length; i++) {
      const essay = essays[i];
      setMarkingStatus(`Marking essay ${i + 1} of ${essays.length}: ${essay.name}`);

      try {
        const response = await fetch('/api/mark-essay', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            essayText: essay.content,
            essayName: essay.name,
            rubricText: rubric.content,
            feedbackGuidance,
          }),
        });

        const data = await response.json();
        generatedFeedbacks.push({
          name: essay.name,
          feedback: data.feedback,
        });

        setFeedbacks([...generatedFeedbacks]);
      } catch (error) {
        console.error('Error marking essay:', error);
      }

      setMarkingProgress(((i + 1) / essays.length) * 100);
    }

    // Generate class feedback
    setMarkingStatus('Generating class overall feedback...');
    try {
      const response = await fetch('/api/class-feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          allFeedbacks: generatedFeedbacks,
          rubricText: rubric.content,
        }),
      });

      const data = await response.json();
      setClassFeedback(data.classFeedback);
    } catch (error) {
      console.error('Error generating class feedback:', error);
    }

    setMarkingStatus('Marking complete!');
    setIsMarking(false);
  };

  const downloadFeedback = (feedback: Feedback) => {
    const blob = new Blob([feedback.feedback], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${feedback.name}.feedback.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadClassFeedback = () => {
    const blob = new Blob([classFeedback], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'class_overall.feedback.md';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="h-6 w-6" />
            <h1 className="text-2xl font-bold">Automatic Essay Marking System</h1>
          </div>
          <ThemeToggle />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="upload" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="upload">
              <Upload className="h-4 w-4 mr-2" />
              Load & Marking
            </TabsTrigger>
            <TabsTrigger value="individual">
              <FileText className="h-4 w-4 mr-2" />
              Individual Feedback
            </TabsTrigger>
            <TabsTrigger value="class">
              <BarChart3 className="h-4 w-4 mr-2" />
              Class Feedback
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Upload Files</CardTitle>
                <CardDescription>
                  Upload student essays, rubrics, and feedback guidance to begin automatic marking
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium flex items-center gap-2">
                      <FileText className="h-4 w-4" />
                      Student Essays (.txt)
                    </label>
                    <input
                      type="file"
                      accept=".txt"
                      multiple
                      onChange={handleEssaysUpload}
                      className="w-full px-3 py-2 border rounded-md text-sm bg-background"
                    />
                    {essays.length > 0 && (
                      <p className="text-sm text-muted-foreground">
                        {essays.length} essay(s) loaded
                      </p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium flex items-center gap-2">
                      <BookOpen className="h-4 w-4" />
                      Rubrics (.md)
                    </label>
                    <input
                      type="file"
                      accept=".md"
                      multiple
                      onChange={handleRubricsUpload}
                      className="w-full px-3 py-2 border rounded-md text-sm bg-background"
                    />
                    {rubrics.length > 0 && (
                      <p className="text-sm text-muted-foreground">
                        {rubrics.length} rubric(s) loaded
                      </p>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Feedback Guidance (.md)</label>
                  <input
                    type="file"
                    accept=".md"
                    onChange={handleFeedbackGuidanceUpload}
                    className="w-full px-3 py-2 border rounded-md text-sm bg-background"
                  />
                  {feedbackGuidance && (
                    <p className="text-sm text-muted-foreground">
                      Feedback guidance loaded
                    </p>
                  )}
                </div>

                {rubrics.length > 0 && (
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Select Rubric for Marking</label>
                    <Select value={selectedRubric} onValueChange={setSelectedRubric}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a rubric" />
                      </SelectTrigger>
                      <SelectContent>
                        {rubrics.map((rubric) => (
                          <SelectItem key={rubric.name} value={rubric.name}>
                            {rubric.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}

                <div className="pt-4">
                  <Button
                    onClick={startMarking}
                    disabled={isMarking || essays.length === 0 || !selectedRubric || !feedbackGuidance}
                    className="w-full"
                    size="lg"
                  >
                    {isMarking ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Marking in Progress...
                      </>
                    ) : (
                      'Start Automatic Marking'
                    )}
                  </Button>
                </div>

                {isMarking && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>{markingStatus}</span>
                      <span>{Math.round(markingProgress)}%</span>
                    </div>
                    <Progress value={markingProgress} />
                  </div>
                )}
              </CardContent>
            </Card>

            {feedbacks.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Marking Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Successfully marked {feedbacks.length} essay(s)
                  </p>
                  <p className="text-sm text-green-600 mt-2">
                    {markingStatus}
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="individual" className="space-y-6">
            {feedbacks.length === 0 ? (
              <Card>
                <CardContent className="pt-6">
                  <p className="text-center text-muted-foreground">
                    No feedback generated yet. Please run automatic marking first.
                  </p>
                </CardContent>
              </Card>
            ) : (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Select Student Essay</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Select value={selectedFeedback} onValueChange={setSelectedFeedback}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a student essay" />
                      </SelectTrigger>
                      <SelectContent>
                        {feedbacks.map((feedback) => (
                          <SelectItem key={feedback.name} value={feedback.name}>
                            {feedback.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </CardContent>
                </Card>

                {selectedFeedback && (
                  <Card>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle>Feedback for: {selectedFeedback}</CardTitle>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            const feedback = feedbacks.find(f => f.name === selectedFeedback);
                            if (feedback) downloadFeedback(feedback);
                          }}
                        >
                          <Download className="h-4 w-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <Textarea
                        value={feedbacks.find(f => f.name === selectedFeedback)?.feedback || ''}
                        readOnly
                        className="min-h-[500px] font-mono text-sm"
                      />
                    </CardContent>
                  </Card>
                )}
              </>
            )}
          </TabsContent>

          <TabsContent value="class" className="space-y-6">
            {!classFeedback ? (
              <Card>
                <CardContent className="pt-6">
                  <p className="text-center text-muted-foreground">
                    No class feedback generated yet. Please run automatic marking first.
                  </p>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Class Performance Analysis</CardTitle>
                      <CardDescription>Overall insights and recommendations</CardDescription>
                    </div>
                    <Button variant="outline" size="sm" onClick={downloadClassFeedback}>
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <Textarea
                      value={classFeedback}
                      readOnly
                      className="min-h-[600px] font-mono text-sm"
                    />
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </main>

      <footer className="border-t mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="text-sm text-muted-foreground space-y-2">
            <p className="font-semibold">About this Application</p>
            <p>
              This application provides automated essay marking using AI. Upload your student essays,
              rubrics, and feedback guidance to generate comprehensive feedback for each student and
              class-level insights.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <p className="font-medium">Essays loaded:</p>
                <p>{essays.length}</p>
              </div>
              <div>
                <p className="font-medium">Rubrics loaded:</p>
                <p>{rubrics.length}</p>
              </div>
              <div>
                <p className="font-medium">Feedback generated:</p>
                <p>{feedbacks.length}</p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
