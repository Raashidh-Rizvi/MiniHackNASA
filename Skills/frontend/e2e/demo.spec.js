import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
test('local signup journey and accessibility',async({page})=>{
  test.skip(!!process.env.TARGET_URL,'Demo journey applies only to the bundled fixture; write app-specific journeys for your target.');
  await page.goto('/'); await page.getByLabel('Email',{exact:true}).fill('learner@example.test');
  await page.getByRole('button',{name:'Join'}).click(); await expect(page.getByRole('status')).toHaveText('Thanks for joining');
  expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
});
test('page accessibility',async({page})=>{
  await page.goto('/'); expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
});
test('visual baseline',async({page})=>{
  await page.goto('/'); await expect(page).toHaveScreenshot('homepage.png',{fullPage:true});
});
