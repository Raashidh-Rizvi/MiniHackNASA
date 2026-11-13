import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Signup } from '../src/Signup.jsx';
import { discount } from '../src/discount.js';
describe('pricing boundary rules', () => {
  it('calculates discounts and rounds currency', () => {
    expect(discount(100, 20)).toBe(80); expect(discount(10, 0)).toBe(10);
    expect(discount(10, 100)).toBe(0); expect(discount(0, 20)).toBe(0);
    expect(discount(9.99, 15)).toBe(8.49);
  });
  it('rejects invalid totals and percentages', () => {
    for (const args of [[-1, 20], [10, -1], [10, 101]]) expect(() => discount(...args)).toThrow(RangeError);
  });
});
it('validates before submitting and accepts a corrected email', async () => {
  const submit = vi.fn(); const user = userEvent.setup(); render(<Signup onSubmit={submit} />);
  await user.click(screen.getByRole('button', { name: 'Join' }));
  expect(screen.getByRole('alert')).toHaveTextContent('Enter a valid email'); expect(submit).not.toHaveBeenCalled();
  await user.type(screen.getByLabelText('Email'), 'learner@example.test');
  await user.click(screen.getByRole('button', { name: 'Join' }));
  expect(submit).toHaveBeenCalledWith('learner@example.test'); expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});
